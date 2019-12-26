import re
import javalang


def find_method(method_node, filter):
    sub_api_seq = []
    for node in method_node.arguments:
        if isinstance(node, javalang.tree.MethodInvocation):
            api = [filter.get(node.qualifier, node.qualifier),
                   node.member]
            sub_api_seq.append(api)
            sub_api_seq.extend(find_method(node, filter))

        if isinstance(node, javalang.tree.ClassCreator):
            api = [node.type.name, 'new']
            sub_api_seq.append(api)
            sub_api_seq.extend(find_method(node, filter))
    return sub_api_seq


def check_selectors(node, s_filter):
    select_api_seq = []
    if node.selectors is not None:
        for sel in node.selectors:
            if isinstance(sel, javalang.tree.MethodInvocation):
                if node.qualifier is None:
                    select_api_seq.append([node.type.name, sel.member])
                else:
                    select_api_seq.append(
                        [s_filter.get(node.qualifier, node.qualifier),
                         sel.member])
    return select_api_seq


class FeatureExtractor:
    def __init__(self, code):
        self.code = code

    def get_api_sequence(self):
        code_str = "package javalang.temp.com; class Temp {%s}" % self.code
        api_seq = []
        tree = javalang.parse.parse(code_str)
        identifier_filter = {}
        for _, node in tree:
            if isinstance(node, javalang.tree.FormalParameter):
                identifier_filter[node.name] = node.type.name

            if isinstance(node, javalang.tree.LocalVariableDeclaration):
                for dec in node.declarators:
                    identifier_filter[dec.name] = node.type.name

            if isinstance(node, javalang.tree.ClassCreator):
                api = [node.type.name, 'new']
                api_seq.append(api)
                api_seq.extend(check_selectors(node, identifier_filter))

            if isinstance(node, javalang.tree.MethodInvocation):
                if node.qualifier == '':
                    continue

                if node.qualifier is None:
                    if len(api_seq) == 0:
                        continue
                    node.qualifier = api_seq[-1][0]

                sub_api_seq = find_method(node, identifier_filter)
                sub_api_seq.append(
                    [identifier_filter.get(node.qualifier, node.qualifier),
                     node.member])
                api_seq.extend(sub_api_seq)
                api_seq.extend(check_selectors(node, identifier_filter))
        api_seq = [' '.join(item) for item in api_seq]
        return ' '.join(api_seq)