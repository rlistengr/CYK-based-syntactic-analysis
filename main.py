class my_CYK(object):
    def __init__(self, non_ternimal, terminal, rules_prob, start_prob):
        '''建立一个CYK算法的对象
        最重要的是对rule的处理，因为将会使用CYK算法，
        所以需要建立一个key值为分解后的结果，value为组合之后的结果和概率
        '''
        self.non_terminal = non_ternimal
        self.terminal = terminal
        self.start_symbol = start_prob

        new_rule = {}
        # 对rules做一定处理，修改为以分解后的结果为key，方便查找
        for left in rules_prob:
            for right in rules_prob[left]:
                if new_rule.get(right) is None:
                    new_rule[right] = {}
                new_rule[right][left] = rules_prob[left][right]

        self.rules_prob = new_rule

    def parse_sentence(self, sentence):
        # parse the sentence with CYK algoritm
        '''
        首先生成一个大小为（1到字符个数之和）的数组，每个成员代表一个树节点。
        每个树节点是一个dict，保存以该节点为root的语法数。
        每个节点计算时，从离自己一行的节点开始，
        行号         节点号（数组下标，0号不使用）
        1              1
        2            2   3
        3          4   5   6
        4        7   8   9   10
        比如节点2第一次取离自己一行的4和最后一行的9，第二次取离自己两行的7和最后第二行的5，因为第一个元素已到最后一行，结束遍历。
        '''
        word_list = sentence.split()
        row = len(word_list)
        first_list = [0, 1]

        # 生成每一行的第一个元素的链表
        for i in range(2, row + 1):
            first_list.append(first_list[i - 1] + (i - 1))

        # 生成树
        gram_tree = [{} for i in range(sum(range(row + 1)))]
        gram_tree.append({})

        # 先对最后一行做初始化
        for j in range(row):
            # 如果有单词不在单词表中则抛出异常
            if word_list[j] not in self.terminal:
                raise Exception('word(%s) is not in vacobulary', word_list[j])

            # 遍历该单词的所有可能情况
            for left in self.rules_prob[((word_list[j]),)]:
                gram_tree[first_list[row] + j][left] = [self.rules_prob[((word_list[j]),)][left], (0,0,0,0)]
                
        # 从倒数第二行开始遍历
        reverse_index = list(range(row))
        reverse_index.reverse()
        # 第i行
        for i in reverse_index:
            # 第j个元素
            for j in range(i):
                # 从下面一行开始到最后一行
                for k in range(i+1,row+1):
                    # 第k行第j个元素
                    left = gram_tree[first_list[k]+j]
                    # 倒数第k-j行即row-(k-i)+1第j+row-(k+i)+1-i个元素
                    right = gram_tree[first_list[row-k+i+1]+j+row-k+1]
                    if len(left) == 0 or len(right) == 0:
                        continue
                    # 取left和right的每一种可能进行组合
                    for x in left:
                        for y in right:
                            if ((x, y)) in self.rules_prob:
                                # 获取((x,y))的每一种可能
                                for z in self.rules_prob[((x, y))]:
                                    tmp = round(self.rules_prob[((x, y))][z] * left[x][0] * right[y][0],10)
                                    # 如果当前已有则需要比较大小
                                    if gram_tree[first_list[i]+j].get(z) is not None:
                                        if tmp > gram_tree[first_list[i]+j][z][0]:
                                            gram_tree[first_list[i] + j][z] = [tmp, (k, j, row-k+i+1, j+row-k+1)]
                                        elif tmp == gram_tree[first_list[i]+j][z][0]:
                                            # 相等再加一个节点的情况，
                                            gram_tree[first_list[i] + j][z].append((k, j, row-k+i+1, j+row-k+1))
                                    else:
                                        gram_tree[first_list[i]+j][z] = [tmp, (k, j, row-k+i+1, j+row-k+1)]


        # print the result with tree structure
        # 遍历生成的树，打印结果
        self._parse_result(1,0,1,gram_tree,first_list)

        # print the probability for most probable parsing
        print('the probability for most probable parsing: ', gram_tree[1]['S'][0])

    def _parse_result(self, left_idx, right_idx, idx, gram_tree,first_list):
        """
        print the result with tree- structure
        """
        if 0 != left_idx:
            for i in gram_tree[left_idx]:
                print('-' * idx, i)
                for j in range(1, len(gram_tree[left_idx][i])):
                    if j > 1:
                        # 说明有多种情况，打印一段分隔符表示从这一级开始还有一种情况,
                        # 同时打出上级名字和标明是左还是右
                        print('='*30, 'left', i)
                    child = gram_tree[left_idx][i][j]
                    self._parse_result(first_list[child[0]]+child[1], first_list[child[2]]+child[3],idx+1,gram_tree,first_list)
        if 0 != right_idx:
            for i in gram_tree[right_idx]:
                print('-'*idx,i)
                for j in range(1, len(gram_tree[right_idx][i])):
                    if j > 1:
                        # 说明有多种情况，打印一段分隔符表示从这一级开始还有一种情况
                        print('='*30, 'right', i)
                    child = gram_tree[right_idx][i][j]
                    self._parse_result(first_list[child[0]]+child[1], first_list[child[2]]+child[3],idx+1,gram_tree,first_list)


def main(sentence):
    non_terminal = {'S', 'NP', 'VP', 'PP', 'DT', 'Vi', 'Vt', 'NN', 'IN'}
    start_symbol = 'S'
    terminal = {'sleeps', 'saw', 'boy', 'girl', 'dog', 'telescope', 'the', 'with', 'in', 'a'}
    rules_prob = {'S': {('NP', 'VP'): 1.0},
                  'VP': {('Vt', 'NP'): 0.8, ('VP', 'PP'): 0.2},
                  'NP': {('DT', 'NN'): 0.8, ('NP', 'PP'): 0.2},
                  'PP': {('IN', 'NP'): 1.0},
                  'Vi': {('sleeps',): 1.0},
                  'Vt': {('saw',): 1.0},
                  'NN': {('boy',): 0.1, ('girl',): 0.1, ('telescope',): 0.3, ('dog',): 0.5},
                  'DT': {('the',): 0.5, ('a',): 0.5},
                  'IN': {('with',): 0.6, ('in',): 0.4},
                  }
    cyk = my_CYK(non_terminal, terminal, rules_prob, start_symbol)
    cyk.parse_sentence(sentence)


sentence = "the boy saw the dog with a telescope"
main(sentence)