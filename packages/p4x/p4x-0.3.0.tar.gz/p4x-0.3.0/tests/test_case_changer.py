from p4x import case_changer

__author__ = 'Philipp Tempel'
__email__ = 'p.tempel@tudelft.nl'


class CaseChangerTestSuite(object):

    @pytest.mark.parametrize(
                ('string', 'expected'),
                (
                        ('', ''),
                        ('test', 'test'),
                        ('test string', 'testString'),
                        ('Test string', 'testString'),
                        ('test String', 'testString'),
                        ('Test String', 'testString'),
                        ('testv2', 'testv2'),
                        ('Testv2', 'testv2'),
                        ('TestV2', 'testV2'),
                        ('_test_string_', 'testString'),
                        ('version 1.2.34', 'version_1_2_34'),
                        ('version 1.23.4', 'version_1_23_4'),
                )
        )
    def test_camel_case(string, expected):
        assert camel_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'Test'),
                    ('test string', 'Test String'),
                    ('Test string', 'Test String'),
                    ('test String', 'Test String'),
                    ('Test String', 'Test String'),
                    ('testv2', 'Testv2'),
                    ('Testv2', 'Testv2'),
                    ('TestV2', 'Test V2'),
                    ('_test_string_', 'Test String'),
                    ('version 1.2.34', 'Version 1 2 34'),
                    ('version 1.23.4', 'Version 1 23 4'),
            )
    )
    def test_capital_case(string, expected):
        assert capital_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'TEST'),
                    ('test string', 'TEST_STRING'),
                    ('Test string', 'TEST_STRING'),
                    ('test String', 'TEST_STRING'),
                    ('Test String', 'TEST_STRING'),
                    ('test.string', 'TEST_STRING'),
                    ('testv2', 'TESTV2'),
                    ('Testv2', 'TESTV2'),
                    ('TestV2', 'TEST_V2'),
                    ('_test_string_', 'TEST_STRING'),
                    ('version 1.2.34', 'VERSION_1_2_34'),
                    ('version 1.23.4', 'VERSION_1_23_4'),
            )
    )
    def test_constant_case(string, expected):
        assert constant_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'test'),
                    ('test string', 'test.string'),
                    ('Test string', 'test.string'),
                    ('test String', 'test.string'),
                    ('Test String', 'test.string'),
                    ('test.string', 'test.string'),
                    ('testv2', 'testv2'),
                    ('Testv2', 'testv2'),
                    ('TestV2', 'test.v2'),
                    ('_test_string_', 'test.string'),
                    ('version 1.2.34', 'version.1.2.34'),
                    ('version 1.23.4', 'version.1.23.4'),
            )
    )
    def test_dot_case(string, expected):
        assert dot_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'Test'),
                    ('test string', 'Test-String'),
                    ('Test string', 'Test-String'),
                    ('test String', 'Test-String'),
                    ('Test String', 'Test-String'),
                    ('testv2', 'Testv2'),
                    ('Testv2', 'Testv2'),
                    ('TestV2', 'Test-V2'),
                    ('_test_string_', 'Test-String'),
                    ('version 1.2.34', 'Version-1-2-34'),
                    ('version 1.23.4', 'Version-1-23-4'),
            )
    )
    def test_header_case(string, expected):
        assert header_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'test'),
                    ('test string', 'test string'),
                    ('Test string', 'test string'),
                    ('test String', 'test string'),
                    ('Test String', 'test string'),
                    ('testv2', 'testv2'),
                    ('Testv2', 'testv2'),
                    ('TestV2', 'test v2'),
                    ('_test_string_', 'test string'),
                    ('version 1.2.34', 'version 1 2 34'),
                    ('version 1.23.4', 'version 1 23 4'),
            )
    )
    def test_no_case(string, expected):
        assert no_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'test'),
                    ('test string', 'test-string'),
                    ('Test string', 'test-string'),
                    ('test String', 'test-string'),
                    ('Test String', 'test-string'),
                    ('test.string', 'test-string'),
                    ('testv2', 'testv2'),
                    ('Testv2', 'testv2'),
                    ('TestV2', 'test-v2'),
                    ('_test_string_', 'test-string'),
                    ('version 1.2.34', 'version-1-2-34'),
                    ('version 1.23.4', 'version-1-23-4'),
            )
    )
    def test_param_case(string, expected):
        assert param_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'Test'),
                    ('test string', 'TestString'),
                    ('Test string', 'TestString'),
                    ('test String', 'TestString'),
                    ('Test String', 'TestString'),
                    ('test.string', 'TestString'),
                    ('testv2', 'Testv2'),
                    ('Testv2', 'Testv2'),
                    ('TestV2', 'TestV2'),
                    ('_test_string_', 'TestString'),
                    ('version 1.2.34', 'Version_1_2_34'),
                    ('version 1.23.4', 'Version_1_23_4'),
            )
    )
    def test_pascal_case(string, expected):
        assert pascal_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'test'),
                    ('test string', 'test/string'),
                    ('Test string', 'test/string'),
                    ('test String', 'test/string'),
                    ('Test String', 'test/string'),
                    ('test.string', 'test/string'),
                    ('testv2', 'testv2'),
                    ('Testv2', 'testv2'),
                    ('TestV2', 'test/v2'),
                    ('_test_string_', 'test/string'),
                    ('version 1.2.34', 'version/1/2/34'),
                    ('version 1.23.4', 'version/1/23/4'),
            )
    )
    def test_path_case(string, expected):
        assert path_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'Test'),
                    ('test string', 'Test string'),
                    ('Test string', 'Test string'),
                    ('test String', 'Test string'),
                    ('Test String', 'Test string'),
                    ('test.string', 'Test string'),
                    ('testv2', 'Testv2'),
                    ('Testv2', 'Testv2'),
                    ('TestV2', 'Test v2'),
                    ('_test_string_', 'Test string'),
                    ('version 1.2.34', 'Version 1 2 34'),
                    ('version 1.23.4', 'Version 1 23 4'),
            )
    )
    def test_sentence_case(string, expected):
        assert sentence_case(string) == expected


    @pytest.mark.parametrize(
            ('string', 'expected'),
            (
                    ('', ''),
                    ('test', 'test'),
                    ('test string', 'test_string'),
                    ('Test string', 'test_string'),
                    ('test String', 'test_string'),
                    ('Test String', 'test_string'),
                    ('test.string', 'test_string'),
                    ('testv2', 'testv2'),
                    ('Testv2', 'testv2'),
                    ('TestV2', 'test_v2'),
                    ('_test_string_', 'test_string'),
                    ('version 1.2.34', 'version_1_2_34'),
                    ('version 1.23.4', 'version_1_23_4'),
            )
    )
    def test_snake_case(string, expected):
        assert snake_case(string) == expected


if __name__ == "__main__":
    pytest.main()
