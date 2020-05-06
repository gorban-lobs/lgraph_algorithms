from queue import Queue
from lgraph import LGraph


def stack_processing(trace_stack, cur_trace):
    traces = (
        {'trace_type': 'round', 'open': '(', 'closed': ')'},
        {'trace_type': 'square', 'open': '[', 'closed': ']'}
    )
    for trace in traces:
        trace_type = trace['trace_type']
        # if cur_trace[trace_type][0]:
        if cur_trace[trace_type][0] == trace['open']:
            trace_stack[trace_type].append(cur_trace[trace_type])
        elif cur_trace[trace_type][0] == trace['closed']:
            if len(trace_stack[trace_type]) == 0 or \
                    trace_stack[trace_type][-1][1] != \
                    cur_trace[trace_type][1]:
                return False
            else:
                trace_stack[trace_type].pop()
    return True


def rest_direct(vertex, trace_stack, passed_edges, determ_vertexes, finals):
    fst_label_set = set()
    if vertex.name not in determ_vertexes:
        determ_vertexes[vertex.name] = {'is_determ': True, 
                                        'fst_labels_set': set()}
    for edge in vertex.edges:
        new_passed_edges = passed_edges.copy()
        if (edge.beg.name, edge.end.name) in passed_edges:
            # print('return', vertex.name)
            continue
        else:
            new_passed_edges.add((edge.beg.name, edge.end.name))

        if edge.end in finals:
            # TODO make smth with finals
            fst_label_set.add('eps')
            continue
        direct_set = set()
        new_stack = trace_stack.copy()
        if stack_processing(new_stack,
                            {'round': edge.round_trace, 
                             'square': edge.round_trace}):
            if edge.label:
                if rest_direct(edge.end,
                               new_stack,
                               new_passed_edges,
                               determ_vertexes,
                               finals):
                    direct_set.add(edge.label)
            else:
                for label in rest_direct(edge.end, 
                                         new_stack,
                                         new_passed_edges,
                                         determ_vertexes,
                                         finals):
                    if label in direct_set:
                        determ_vertexes[vertex.name]['is_determ'] = False
                    direct_set.add(label)
        fst_label_size = len(fst_label_set)
        fst_label_set = fst_label_set.union(direct_set)
        # print('fst_label_set:', fst_label_set)
        if len(fst_label_set) != fst_label_size + len(direct_set):
            determ_vertexes[vertex.name]['is_determ'] = False
        # print((edge.beg.name, edge.end.name), fst_label_set)
    determ_vertexes[vertex.name]['fst_labels_set'] = \
        determ_vertexes[vertex.name]['fst_labels_set'].union(fst_label_set)
    return fst_label_set


def create_direct_dict(lgraph):
    # TODO many initial vertexes
    determ_vertexes = dict()
    for init_vert in lgraph.initials:
        vertex = list(init_vert.edges)[0].end
        trace_stack = {'round': [], 'square': []}
        rest_direct(vertex, trace_stack, set(), determ_vertexes, lgraph.finals)
    return determ_vertexes
