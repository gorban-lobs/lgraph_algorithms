from copy import deepcopy
from lgraph import LGraph, Vertex, Edge


class Edge(Edge):
    def __init__(self,
                 beg_vertex: Vertex,
                 end_vertex: Vertex,
                 label='',
                 round_trace=('', 0),
                 square_trace=('', 0)):
        self.__beg = beg_vertex
        self.__end = end_vertex
        self.__label = label
        if isinstance(round_trace, str):
            round_trace = (round_trace, 0)
        if isinstance(square_trace, str):
            square_trace = (square_trace, 0)

        if not (isinstance(round_trace, tuple)
                and isinstance(square_trace, tuple)
                and len(round_trace) == len(square_trace) == 2
                and isinstance(round_trace[1], int)
                and isinstance(square_trace[1], int)):
            raise ValueError(
                'Bracket trace should be a tuple object '
                'with a bracket as first element and its number as a second.')

        self.__round_trace = round_trace
        self.__square_trace = square_trace


class ConjLGraph(LGraph):
    def __init__(self, *args):
        super().__init__(*args)

    def add_edge(self,
                 beg_vtx_name: str,
                 end_vtx_name: str,
                 label='',
                 round_trace=('', 0),
                 square_trace=('', 0)):
        if label not in self.alphabet:
            raise ValueError(f'Edge label "{label}"" is not from the alphabet.')

        beg_vtx = self.get_vertex(beg_vtx_name)
        end_vtx = self.get_vertex(end_vtx_name)
        edg = Edge(
            beg_vtx, end_vtx, label=label,
            round_trace=round_trace, square_trace=square_trace)
        self._LGraph__edges.add(edg)
        beg_vtx.add_edge(edg)


def stack_processing(trace_stack, cur_trace):
    traces = (
        {'trace_type': 'round', 'open': '(', 'closed': ')'},
        {'trace_type': 'square', 'open': '[', 'closed': ']'}
    )
    for trace in traces:
        trace_type = trace['trace_type']
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


def rest_direct(vertex, trace_stack, passed_edges, determ_vertices, finals,
                cycle_iterations):
    fst_label_set = set()
    if vertex.name not in determ_vertices:
        determ_vertices[vertex.name] = {'is_determ': True, 
                                        'fst_labels_set': set()}
    for edge in vertex.edges:
        new_passed_edges = passed_edges.copy()
        cur_edge = (edge.beg.name, edge.end.name)
        if cur_edge in new_passed_edges and \
                new_passed_edges[cur_edge] == cycle_iterations:
            continue
        else:
            if cur_edge not in new_passed_edges:
                new_passed_edges[cur_edge] = 1
            else:
                new_passed_edges[cur_edge] += 1

        if edge.end in finals:
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
                               determ_vertices,
                               finals,
                               cycle_iterations):
                    direct_set.add(edge.label)
            else:
                for label in rest_direct(edge.end, 
                                         new_stack,
                                         new_passed_edges,
                                         determ_vertices,
                                         finals,
                                         cycle_iterations):
                    if label in direct_set:
                        determ_vertices[vertex.name]['is_determ'] = False
                    direct_set.add(label)
        fst_label_size = len(fst_label_set)
        fst_label_set = fst_label_set.union(direct_set)
        if len(fst_label_set) != fst_label_size + len(direct_set):
            determ_vertices[vertex.name]['is_determ'] = False
    determ_vertices[vertex.name]['fst_labels_set'] = \
        determ_vertices[vertex.name]['fst_labels_set'].union(fst_label_set)
    if 'eps' in determ_vertices[vertex.name]['fst_labels_set'] and \
            len(determ_vertices[vertex.name]['fst_labels_set']) > 1:
        determ_vertices[vertex.name]['fst_labels_set'].remove('eps')
    return fst_label_set


def create_direct_dict(lgraph, cycle_iterations=1):
    if cycle_iterations < 1:
        print("Wrong cycle_iterations param value")
        raise ValueError
    # many initial vertices
    determ_vertices = dict()
    for init_vert in lgraph.initials:
        vertex = list(init_vert.edges)[0].end
        trace_stack = {'round': [], 'square': []}
        passed_edges = dict()
        rest_direct(vertex, trace_stack, passed_edges, 
                    determ_vertices, lgraph.finals, cycle_iterations)
    return determ_vertices


def is_determinated(direct_dict):
    for vert in direct_dict.values():
        if not vert['is_determ']:
            return False
    return True


def rest_conjugation(vertex1, vertex2,
                     lgraph1, lgraph2,
                     conj_graph, passed_edges):
    for edge1 in vertex1.edges:
        success_flag = False
        for edge2 in vertex2.edges:
            if edge1.label == edge2.label:
                success_flag = True
                end_vertex1, end_vertex2 = edge1.end, edge2.end
                edge_beg = f'{vertex1.name}|{vertex2.name}'
                edge_end = f'{end_vertex1.name}|{end_vertex2.name}'
                if (edge_beg, edge_end) not in passed_edges:
                    edge_round_trace = (
                        '(|'
                        f'{edge1.round_trace[0]},{edge1.round_trace[1]}|'
                        f'{edge2.round_trace[0]},{edge2.round_trace[1]}', 0)
                    edge_square_trace = (
                        '[|'
                        f'{edge1.square_trace[0]},{edge1.square_trace[1]}|'
                        f'{edge2.square_trace[0]},{edge2.square_trace[1]}', 0)
                    if edge_end not in [vert.name 
                                        for vert in conj_graph.vertexes]:
                        conj_graph.add_vertex(edge_end)
                    conj_graph.add_edge(edge_beg, edge_end,
                                        label=edge1.label,
                                        round_trace=edge_round_trace,
                                        square_trace=edge_square_trace)
                    print(edge_beg, edge_end)
                    passed_edges.add((edge_beg, edge_end))
                    if not rest_conjugation(end_vertex1, end_vertex2,
                                            lgraph1, lgraph2,
                                            conj_graph, passed_edges):
                        return False
                else:
                    success_flag = True
        if not success_flag:
            return False
    return True


def create_conjugation_lgraph(lgraph1, lgraph2):
    conj_graph = ConjLGraph()
    passed_edges = set()
    success_flag = True
    for initial1 in lgraph1.initials:
        for initial2 in lgraph2.initials:
            for edge1 in initial1.edges:
                for edge2 in initial2.edges:
                    vertex1, vertex2 = edge1.end, edge2.end
                    conj_graph.add_vertex(f'{vertex1.name}|{vertex2.name}')
                    success_flag = rest_conjugation(vertex1, vertex2,
                                                    lgraph1, lgraph2,
                                                    conj_graph, passed_edges) \
                                   or success_flag
    if success_flag:
        print('Creation of conjugation L-graph: Success')
        return conj_graph
    else:
        print('Creation of conjugation L-graph: Failure')
        return None
