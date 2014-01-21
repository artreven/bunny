from bunny_exploration.term_parser import parse_str, flatten, term_parse, make_input

class TestParser:
    @classmethod
    def setup_class(self):
        self.text1 = "-x*a"
        self.text2 = "(-x)*(a*z)"
        self.text3 = "-(x*a)"
        self.text4 = "-(-x)*a"
        self.text5 = "x"
        self.parsed = term_parse(self.text1)[0]
        
    @classmethod
    def teardown_class(self):
        pass
    
    def test_parser(self):
        assert parse_str(self.text1) == ('-x*a', 2, 3, [0, 0], [1, 3, 1], [1, 2, 0])
        assert parse_str(self.text2) == ('(-x)*(a*z)', 3, 4, [0, 0, 2], [3, 5, 1, 2], [1, 2, 0, 2])
        assert parse_str(self.text3) == ('-(x*a)', 2, 3, [0, 0], [5, 3, 1], [1, 2, 0])
        assert parse_str(self.text4) == ('-(-x)*a', 2, 4, [0, 0], [3, 1, 4, 1], [1, 1, 2, 0])
        assert parse_str(self.text5) == ('x', 1, 0, [0], [], [])
        
    def test_flatten(self):
        assert flatten([[1,2], 3]) == [1, 2, 3]
        assert (flatten(('-x*a', 2, 3, [0, 0], [1, 3, 1], [1, 2, 0]))
                == ['-x*a', 2, 3, 0, 0, 1, 3, 1, 1, 2, 0])
        assert (flatten(self.parsed, track=True)
                == [('val', 1), ('exp', 2), ('sym', 3), ('var', 4), ('un', 5),
                    ('-', 5), ('x', 4), ('bin', 3), ('*', 3), ('exp', 3),
                    ('sym', 4), ('nul', 5), ('a', 5)])
        assert (flatten(parse_str(self.text1))
                == ['-x*a', 2, 3, 0, 0, 1, 3, 1, 1, 2, 0])
        
    def test_make_input(self):
        assert (make_input(True, self.text1, self.text3)
                == ['2', '-x*a', '2', '3', '0', '0', '1', '3', '1', '1', '2',
                    '0', '-(x*a)', '2', '3', '0', '0', '5', '3', '1', '1', '2', '0'])
        assert (make_input(False, self.text1, self.text3)
                == ['2', '2', '3', '0', '0', '1', '3', '1', '1', '2', '0', '2',
                    '3', '0', '0', '5', '3', '1', '1', '2', '0'])