import sys
from antlr4 import *
from antlr4.tree.Trees import Trees
from antlr4.Utils import escapeWhitespace

from PhpLexer import PhpLexer
from PhpParser import PhpParser

import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint

class WriteTreeListener(ParseTreeListener):
    def visitTerminal(self, node:TerminalNode):
        print ("Visit Terminal: " + str(node) + " - " + repr(node))

class CFGNode:
    def __init__(self, label):
        self.label = label

def generate_cfg(tree):

    cfg = nx.DiGraph()
    ruleNames = tree.parser.ruleNames
    
    def traverse(node):
        nonlocal cfg
        label = escapeWhitespace(Trees.getNodeText(node, ruleNames), False)

        cfg_node = CFGNode(label)
        cfg.add_node(cfg_node.label)

        for child in Trees.getChildren(node):
            child_node = traverse(child)
            cfg.add_edge(cfg_node.label, child_node.label)

        return cfg_node

    traverse(tree)

    return cfg

class CFGGenerator(ParseTreeListener):
    def __init__(self):
        self.cfg = None

    def enterEveryRule(self, ctx):
        if self.cfg is None:
            self.cfg = generate_cfg(ctx)

def visualize_graph(G):
    pos = nx.spring_layout(G, seed=43, k=0.15, iterations=20)


    labels = nx.get_edge_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=8)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')
    plt.show()

def main(argv):
    input_stream = FileStream(argv[1])
    print("Test started for: " + argv[1])
    lexer = PhpLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = PhpParser(stream)
    tree = parser.phpBlock()

    print(Trees.toStringTree(tree, None, parser))

    # ruleNames = parser.ruleNames
    # s = escapeWhitespace(Trees.getNodeText(tree, ruleNames), False)


    # cfg_generator = CFGGenerator()
    # walker = ParseTreeWalker()
    # walker.walk(cfg_generator, tree)

    # cfg = cfg_generator.cfg
    # visualize_graph(cfg)

    

if __name__ == '__main__':
    print("Running")
    main(sys.argv)