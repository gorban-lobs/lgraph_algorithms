from copy import deepcopy
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


def rest_direct(vertex, trace_stack, passed_edges, determ_vertexes, finals,
                cycle_iterations):
    fst_label_set = set()
    # print(determ_vertexes)
    if vertex.name not in determ_vertexes:
        determ_vertexes[vertex.name] = {'is_determ': True, 
                                        'fst_labels_set': set()}
    for edge in vertex.edges:
        new_passed_edges = passed_edges.copy()
        cur_edge = (edge.beg.name, edge.end.name)
        # print(f'{cur_edge} | {new_passed_edges} | {trace_stack}')
        if cur_edge in new_passed_edges and \
                new_passed_edges[cur_edge] == cycle_iterations:
            # new_passed_edges[cur_edge] += 1
            # print('continue')
            continue
        else:
            if cur_edge not in new_passed_edges:
                # print('new')
                new_passed_edges[cur_edge] = 1
            else:
                # print('add')
                new_passed_edges[cur_edge] += 1

        if edge.end in finals:
            # make smth with finals
            fst_label_set.add('eps')
            continue
        direct_set = set()
        new_stack = deepcopy(trace_stack)
        if stack_processing(new_stack,
                            {'round': edge.round_trace, 
                             'square': edge.round_trace}):
            if edge.label:
                if rest_direct(edge.end,
                               new_stack,
                               new_passed_edges,
                               determ_vertexes,
                               finals,
                               cycle_iterations):
                    direct_set.add(edge.label)
            else:
                for label in rest_direct(edge.end, 
                                         new_stack,
                                         new_passed_edges,
                                         determ_vertexes,
                                         finals,
                                         cycle_iterations):
                    if label in direct_set:
                        determ_vertexes[vertex.name]['is_determ'] = False
                    direct_set.add(label)
        fst_label_size = len(fst_label_set)
        fst_label_set = fst_label_set.union(direct_set)
        if len(fst_label_set) != fst_label_size + len(direct_set):
            determ_vertexes[vertex.name]['is_determ'] = False
    determ_vertexes[vertex.name]['fst_labels_set'] = \
        determ_vertexes[vertex.name]['fst_labels_set'].union(fst_label_set)
    return fst_label_set


def create_direct_dict(lgraph, cycle_iterations=1):
    if cycle_iterations < 1:
        print("Wrong cycle_iterations param value")
        raise ValueError
    # many initial vertexes
    determ_vertexes = dict()
    for init_vert in lgraph.initials:
        vertex = list(init_vert.edges)[0].end
        trace_stack = {'round': [], 'square': []}
        passed_edges = dict()
        rest_direct(vertex, trace_stack, passed_edges, 
                    determ_vertexes, lgraph.finals, cycle_iterations)
    return determ_vertexes
