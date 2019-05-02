# CYK-based-syntactic-analysis
使用CYK算法，根据所提供的：非终结符集合、终结符集合、规则集，对输入句子计算句法结构。
比如：
    非终结符集合： {'S', 'NP', 'VP', 'PP', 'DT', 'Vi', 'Vt', 'NN', 'IN'}
    终结符集合 ： 'S'
    终结符集合 ： {'sleeps', 'saw', 'boy', 'girl', 'dog', 'telescope', 'the', 'with', 'in', 'a'}
    规则集 ： {'S': {('NP', 'VP'): 1.0},
                  'VP': {('Vt', 'NP'): 0.8, ('VP', 'PP'): 0.2},
                  'NP': {('DT', 'NN'): 0.8, ('NP', 'PP'): 0.2},
                  'PP': {('IN', 'NP'): 1.0},
                  'Vi': {('sleeps',): 1.0},
                  'Vt': {('saw',): 1.0},
                  'NN': {('boy',): 0.1, ('girl',): 0.1, ('telescope',): 0.3, ('dog',): 0.5},
                  'DT': {('the',): 0.5, ('a',): 0.5},
                  'IN': {('with',): 0.6, ('in',): 0.4},
                  }
    结果：
        - S
        -- NP
        --- DT
        --- NN
        -- VP
        --- VP
        ---- Vt
        ---- NP
        ----- DT
        ----- NN
        --- PP
        ---- IN
        ---- NP
        ----- DT
        ----- NN
        ============================== right VP
        --- Vt
        --- NP
        ---- NP
        ----- DT
        ----- NN
        ---- PP
        ----- IN
        ----- NP
        ------ DT
        ------ NN
        the probability for most probable parsing:  9.216e-05
    其中一个-代表一级，=========代表上一级有多种情况，这里表示二级的右分支VP有多种分析情况，然后接着打印子树下的另一种情形