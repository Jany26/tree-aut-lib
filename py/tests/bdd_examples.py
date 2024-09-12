from bdd.bdd_node import BDDnode
from bdd.bdd_class import BDD

# BDD 1
bdd_1_node_a = BDDnode("a", "x1")
bdd_1_node_b = BDDnode("b", "x2")
bdd_1_node_c = BDDnode("c", "x3")
bdd_1_node_d = BDDnode("d", "x4")
bdd_1_node_e = BDDnode("0", 0)
bdd_1_node_f = BDDnode("1", 1)

bdd_1_node_a.attach(bdd_1_node_b, bdd_1_node_c)
bdd_1_node_b.attach(bdd_1_node_e, bdd_1_node_f)
bdd_1_node_c.attach(bdd_1_node_d, bdd_1_node_e)
bdd_1_node_d.attach(bdd_1_node_f, bdd_1_node_f)
bdd_1 = BDD("test1", bdd_1_node_a)

# BDD 2
bdd_2_node_q0 = BDDnode("e", "x1")
bdd_2_node_q1 = BDDnode("f", "x2")
bdd_2_node_q2 = BDDnode("g", "x3")
bdd_2_node_q3 = BDDnode("h", "x4")
bdd_2_node_q4 = BDDnode("0", 0)
bdd_2_node_q5 = BDDnode("1", 1)

bdd_2_node_q0.attach(bdd_2_node_q1, bdd_2_node_q2)
bdd_2_node_q1.attach(bdd_2_node_q4, bdd_2_node_q5)
bdd_2_node_q2.attach(bdd_2_node_q3, bdd_2_node_q4)
bdd_2_node_q3.attach(bdd_2_node_q5, bdd_2_node_q5)
bdd_2 = BDD("test2", bdd_2_node_q0)

# BDD 3
bdd_3_node_t0 = BDDnode("t0", 0)
bdd_3_node_t1 = BDDnode("t1", 1)
bdd_3_node_n1 = BDDnode("n1", "x4", bdd_3_node_t0, bdd_3_node_t1)
bdd_3_node_n2 = BDDnode("n2", "x2", bdd_3_node_t0, bdd_3_node_t1)
bdd_3_node_n3 = BDDnode("n3", "x1", bdd_3_node_n1, bdd_3_node_n2)
bdd_3 = BDD("test1", bdd_3_node_n3)

# BDD 4
bdd_4_node_t0 = BDDnode("t0", 0)
bdd_4_node_t1 = BDDnode("t1", 1)
bdd_4_node_n1 = BDDnode("n1", "x2", bdd_4_node_t0, bdd_4_node_t1)
bdd_4_node_n2 = BDDnode("n2", "x4", bdd_4_node_t0, bdd_4_node_t1)
bdd_4_node_n3 = BDDnode("n3", "x1", bdd_4_node_n1, bdd_4_node_n2)
bdd_4 = BDD("test2", bdd_4_node_n3)
