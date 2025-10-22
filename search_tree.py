from manim import *

class MinimaxVsAlphaBeta(Scene):
    def construct(self):
        # Step 1: Build a small 2-level tree
        root = Circle(radius=0.3, color=WHITE).shift(UP*2)
        root_label = Text("Max", font_size=20).next_to(root, DOWN)

        left = Circle(radius=0.3, color=BLUE).shift(LEFT*3)
        right = Circle(radius=0.3, color=BLUE).shift(RIGHT*3)
        left_label = Text("Min", font_size=20).next_to(left, DOWN)
        right_label = Text("Min", font_size=20).next_to(right, DOWN)

        edge1 = Line(root.get_bottom(), left.get_top())
        edge2 = Line(root.get_bottom(), right.get_top())

        # Leaves
        l1 = Circle(radius=0.25, color=GREEN).shift(LEFT*4.5 + DOWN*2)
        l2 = Circle(radius=0.25, color=GREEN).shift(LEFT*1.5 + DOWN*2)
        r1 = Circle(radius=0.25, color=GREEN).shift(RIGHT*1.5 + DOWN*2)
        r2 = Circle(radius=0.25, color=GREEN).shift(RIGHT*4.5 + DOWN*2)

        edges_left = [Line(left.get_bottom(), l1.get_top()),
                      Line(left.get_bottom(), l2.get_top())]
        edges_right = [Line(right.get_bottom(), r1.get_top()),
                       Line(right.get_bottom(), r2.get_top())]

        # Draw the whole tree
        self.play(Create(root), Write(root_label))
        self.play(Create(left), Write(left_label), Create(right), Write(right_label))
        self.play(Create(edge1), Create(edge2))
        self.play(Create(l1), Create(l2), Create(r1), Create(r2))
        self.play(*[Create(e) for e in edges_left + edges_right])

        # Step 2: Minimax evaluation (no pruning)
        values = [2, 5, 1, 4]
        leaves = [l1, l2, r1, r2]
        leaf_labels = []
        for i, leaf in enumerate(leaves):
            lbl = Text(str(values[i]), font_size=20).move_to(leaf.get_center())  # CENTERED
            leaf_labels.append(lbl)
            self.play(Write(lbl))

        # Animate min-node evaluation
        left_value = Text(str(min(values[0:2])), font_size=20).move_to(left.get_center())
        self.play(Write(left_value))

        right_value = Text(str(min(values[2:4])), font_size=20).move_to(right.get_center())
        self.play(Write(right_value))

        # Root evaluation
        root_value = Text(str(max(min(values[0:2]), min(values[2:4]))), font_size=20).move_to(root.get_center())
        self.play(Write(root_value))

        # Step 3: Rewind
        self.wait(1)
        self.play(FadeOut(root_value), FadeOut(left_value), FadeOut(right_value))
        self.play(*[FadeOut(lbl) for lbl in leaf_labels])
        self.wait(1)

        # Step 4: Replay with pruning
        leaf_labels = []
        for i, leaf in enumerate(leaves):
            lbl = Text(str(values[i]), font_size=20).move_to(leaf.get_center())
            leaf_labels.append(lbl)

        # Evaluate first branch
        self.play(Write(leaf_labels[0]))
        self.play(Write(leaf_labels[1]))
        left_value = Text(str(min(values[0:2])), font_size=20).move_to(left.get_center())
        self.play(Write(left_value))

        # Evaluate second branch
        self.play(Write(leaf_labels[2]))
        right_value = Text(str(min(values[2:4])), font_size=20).move_to(right.get_center())
        self.play(Write(right_value))

        # Prune r2
        self.play(leaves[3].animate.set_fill(RED, opacity=0.5))
        self.play(Indicate(leaves[3]))
        self.play(FadeIn(Text("Pruned!", font_size=20).next_to(leaves[3], DOWN)))

        # Root result
        root_value = Text(str(max(min(values[0:2]), min(values[2:4]))), font_size=20).move_to(root.get_center())
        self.play(Write(root_value))
