from lgraph import LGraph
from algorithms import stack_processing, create_direct_dict, is_determinated
from algorithms import create_conjugation_lgraph


def test_stack_processing():
    trace_stack = {'round': [('(', 1)], 'square': []}
    cur_trace = {'round': (')', 1), 'square': ''}
    assert stack_processing(trace_stack, cur_trace) == True
    print('1:', trace_stack)

    trace_stack = {'round': [('(', 1)], 'square': []}
    cur_trace = {'round': (')', 2), 'square': ''}
    assert stack_processing(trace_stack, cur_trace) == False
    print('2:', trace_stack)

    trace_stack = {'round': [('(', 1)], 'square': []}
    cur_trace = {'round': (')', 2), 'square': ''}
    assert stack_processing(trace_stack, cur_trace) == False
    print('3:', trace_stack)

    trace_stack = {'round': [('(', 1)], 'square': [('[', 1), ('[', 2)]}
    cur_trace = {'round': (')', 1), 'square': (']', 2)}
    assert stack_processing(trace_stack, cur_trace) == True
    print('4:', trace_stack)

    trace_stack = {'round': [('(', 1)], 'square': []}
    cur_trace = {'round': ('(', 2), 'square': ('[', 3)}
    assert stack_processing(trace_stack, cur_trace) == True
    print('5:', trace_stack)


def test_create_direct_dict():
    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', lg.final_main.name)
    print('0:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('1', '3', label='a')
    print('1:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('1', '3', label='a')
    lg.add_edge('2', lg.final_main.name)
    lg.add_edge('3', 'finals_1')
    print('2:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', lg.final_main.name)
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', 'finals_1')
    print('3:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    print('4:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    lg.add_edge('2', '4', label='b')
    lg.add_edge('4', 'finals_1')
    print('5:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    lg.add_edge('2', '4', label='a')
    lg.add_edge('4', 'finals_1')
    print('6:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2', label='a', round_trace=('(', 1))
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c', round_trace=(')', 1))
    lg.add_edge('2', '4', label='a', round_trace=(')', 2))
    lg.add_edge('4', 'finals_1')
    print('7:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '1', label='a', round_trace=('(', 1))
    lg.add_edge('1', '2', label='b')
    lg.add_edge('2', '3', label='c', round_trace=(')', 1))
    lg.add_edge('3', '4', label='d', round_trace=(')', 1))
    lg.add_edge('4', lg.final_main.name)
    print('8:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '1', label='a', round_trace=('(', 1))
    lg.add_edge('1', '2', label='b')
    lg.add_edge('2', '3', label='c', round_trace=(')', 1))
    lg.add_edge('3', '4', label='d', round_trace=(')', 1))
    lg.add_edge('4', lg.final_main.name)
    print('9:', create_direct_dict(lg, 2))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '1', label='a', round_trace=('(', 1))
    lg.add_edge('1', '2', label='c')
    lg.add_edge('2', '2', label='d', round_trace=(')', 1))
    lg.add_edge('2', lg.final_main.name)
    print('10a:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '1', round_trace=('(', 1))
    lg.add_edge('1', '2', label='c')
    lg.add_edge('2', '2', label='d', round_trace=(')', 1))
    lg.add_edge('2', lg.final_main.name)
    print('10b:', create_direct_dict(lg))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('5')
    lg.add_vertex('6')
    lg.add_vertex('7')
    lg.add_vertex('8')
    lg.add_vertex('9')
    lg.add_vertex('10')
    lg.add_vertex('11')
    lg.add_vertex('finals_2')
    lg.add_vertex('finals_3')
    lg.add_vertex('finals_4')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2')
    lg.add_edge('2', '2', label='k', round_trace=('(', 1))
    lg.add_edge('2', '3', label='m')
    lg.add_edge('3', '3', label='d', round_trace=(')', 1))
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '4', label='a')
    lg.add_edge('4', '4', label='a')
    lg.add_edge('4', '5')
    lg.add_edge('5', '5', label='d')
    lg.add_edge('5', '11', label='a')
    lg.add_edge('11', 'finals_2')
    lg.add_edge('1', '6', label='b')
    lg.add_edge('6', '6', label='m', round_trace=('(', 1))
    lg.add_edge('6', '7', label='n', round_trace=(')', 1))
    lg.add_edge('7', '8', label='n', round_trace=(')', 1))
    lg.add_edge('8', '9', label='n', round_trace=(')', 1))
    lg.add_edge('7', '9', label='k')
    lg.add_edge('9', 'finals_3')
    lg.add_edge('6', '10', label='n', round_trace=(')', 2))
    lg.add_edge('10', 'finals_4')
    print('11:', create_direct_dict(lg))
    print('12:', create_direct_dict(lg, 3))

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '1')
    lg.add_edge('1', '2', label='c')
    lg.add_edge('1', lg.final_main.name)
    lg.add_edge('2', 'finals_1')
    print('13:', create_direct_dict(lg))


def test_is_determ():
    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', lg.final_main.name)
    assert is_determinated(create_direct_dict(lg)) == True

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('1', '3', label='a')
    assert is_determinated(create_direct_dict(lg)) == True

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '2', label='a')
    lg.add_edge('1', '3', label='a')
    lg.add_edge('2', lg.final_main.name)
    lg.add_edge('3', 'finals_1')
    assert is_determinated(create_direct_dict(lg)) == False

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', lg.final_main.name)
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', 'finals_1')
    assert is_determinated(create_direct_dict(lg)) == True

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2', label='a')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    assert is_determinated(create_direct_dict(lg)) == True

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    lg.add_edge('2', '4', label='b')
    lg.add_edge('4', 'finals_1')
    assert is_determinated(create_direct_dict(lg)) == True

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2')
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c')
    lg.add_edge('2', '4', label='a')
    lg.add_edge('4', 'finals_1')
    assert is_determinated(create_direct_dict(lg)) == False

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_vertex('finals_1')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('3', lg.final_main.name)
    lg.add_edge('1', '2', label='a', round_trace=('(', 1))
    lg.add_edge('2', '2', label='a')
    lg.add_edge('2', '3', label='c', round_trace=(')', 1))
    lg.add_edge('2', '4', label='a', round_trace=(')', 2))
    lg.add_edge('4', 'finals_1')
    assert is_determinated(create_direct_dict(lg)) == True

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '1', label='a', round_trace=('(', 1))
    lg.add_edge('1', '2', label='b')
    lg.add_edge('2', '3', label='c', round_trace=(')', 1))
    lg.add_edge('3', '4', label='d', round_trace=(')', 1))
    lg.add_edge('4', lg.final_main.name)
    assert is_determinated(create_direct_dict(lg)) == True

    lg = LGraph()
    lg.add_vertex('1')
    lg.add_vertex('2')
    lg.add_vertex('3')
    lg.add_vertex('4')
    lg.add_edge(lg.initial_main.name, '1')
    lg.add_edge('1', '1', label='a', round_trace=('(', 1))
    lg.add_edge('1', '2', label='b')
    lg.add_edge('2', '3', label='c', round_trace=(')', 1))
    lg.add_edge('3', '4', label='d', round_trace=(')', 1))
    lg.add_edge('4', lg.final_main.name)
    assert is_determinated(create_direct_dict(lg, 2)) == True


def print_vertices(lg):
    for vertex in lg.vertexes:
        print(vertex.name)


def print_edges(lg):
    for edge in lg.edges:
        print(edge.beg.name, edge.end.name, edge.label, 
              edge.round_trace, edge.square_trace)


def test_create_conjugation_lgraph():
    lg1 = LGraph()
    lg1.add_vertex('1')
    lg1.add_vertex('2')
    lg1.add_vertex('3')
    lg1.add_edge(lg1.initial_main.name, '1')
    lg1.add_edge('1', '2', label='a')
    lg1.add_edge('2', '3', label='b')
    lg1.add_edge('3', lg1.final_main.name)

    lg2 = LGraph()
    lg2.add_vertex('4')
    lg2.add_vertex('5')
    lg2.add_vertex('6')
    lg2.add_edge(lg2.initial_main.name, '4')
    lg2.add_edge('4', '5', label='a')
    lg2.add_edge('5', '6', label='b')
    lg2.add_edge('6', lg2.final_main.name)

    conj_lgraph = create_conjugation_lgraph(lg1, lg2)
    print('1:')
    if conj_lgraph:
        print_vertices(conj_lgraph)
        print_edges(conj_lgraph)

    lg1 = LGraph()
    lg1.add_vertex('1')
    lg1.add_vertex('2')
    lg1.add_vertex('3')
    lg1.add_vertex('initials_1')
    lg1.add_edge(lg1.initial_main.name, '1')
    lg1.add_edge('initials_1', '2')
    lg1.add_edge('1', '3', label='a')
    lg1.add_edge('2', '3', label='b')
    lg1.add_edge('3', lg1.final_main.name)

    lg2 = LGraph()
    lg2.add_vertex('4')
    lg2.add_vertex('5')
    lg2.add_vertex('6')
    lg2.add_vertex('initials_2')
    lg2.add_edge(lg2.initial_main.name, '4')
    lg2.add_edge('initials_2', '5')
    lg2.add_edge('4', '6', label='a')
    lg2.add_edge('5', '6', label='b')
    lg2.add_edge('6', lg2.final_main.name)

    conj_lgraph = create_conjugation_lgraph(lg1, lg2)
    print('2:')
    if conj_lgraph:
        print_vertices(conj_lgraph)
        print_edges(conj_lgraph)

    lg1 = LGraph()
    lg1.add_vertex('1')
    lg1.add_vertex('2')
    lg1.add_vertex('3')
    lg1.add_vertex('initials_1')
    lg1.add_edge(lg1.initial_main.name, '1')
    lg1.add_edge('initials_1', '2')
    lg1.add_edge('1', '3', label='a')
    lg1.add_edge('2', '3', label='b')
    lg1.add_edge('3', lg1.final_main.name)

    lg2 = LGraph()
    lg2.add_vertex('4')
    lg2.add_vertex('5')
    lg2.add_vertex('6')
    lg2.add_vertex('initials_2')
    lg2.add_edge(lg2.initial_main.name, '4')
    lg2.add_edge('initials_2', '5')
    lg2.add_edge('4', '6', label='a')
    lg2.add_edge('5', '6', label='b')
    lg2.add_edge('6', lg2.final_main.name)

    conj_lgraph = create_conjugation_lgraph(lg1, lg2)
    print('3:')
    if conj_lgraph:
        print_vertices(conj_lgraph)
        print_edges(conj_lgraph)


if __name__ == '__main__':
    test_create_conjugation_lgraph()
