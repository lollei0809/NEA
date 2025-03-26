from main_code.questions import UnsignedQuestion, SignAndMagnitude, TwosComplement, HexToDec

def test_unsigned_question_generate_question():
    """tests that the generate_question method correctly creates an unsigned binary question"""
    uq = UnsignedQuestion("dtub")
    uq.generate_question()
    assert isinstance(uq.question, int)
    assert 0 <= uq.question <= 255

    uq = UnsignedQuestion("ubtd")
    uq.generate_question()
    assert isinstance(uq.question, str)
    assert len(uq.question) == 8 and set(uq.question).issubset({"0", "1"})


def test_unsigned_question_generate_correct_answer():
    """tests that the correct answer is generated for unsigned binary questions"""
    #normal data
    uq = UnsignedQuestion("dtub")
    uq.question = 5
    uq.generate_correct_answer()
    assert uq.correct_answer == "00000101"

    uq = UnsignedQuestion("ubtd")
    uq.question = "00000101"
    uq.generate_correct_answer()
    assert uq.correct_answer == 5

    #boundary data
    uq = UnsignedQuestion("dtub")
    uq.question = 0
    uq.generate_correct_answer()
    assert uq.correct_answer == "00000000"

    uq = UnsignedQuestion("ubtd")
    uq.question = "00000000"
    uq.generate_correct_answer()
    assert uq.correct_answer == 0


def test_sign_and_magnitude_generate_question():
    """tests that generate_question() correctly creates a sign and magnitude question"""
    sm = SignAndMagnitude("dtsm")
    sm.generate_question()
    assert isinstance(sm.question, int)
    assert -127 <= sm.question <= 127

    sm = SignAndMagnitude("smtd")
    sm.generate_question()
    assert len(sm.question) == 8
    for digit in sm.question:
        assert digit in ["0", "1"]


def test_sign_and_magnitude_generate_correct_answer():
    """tests that the correct answer is generated for sign and magnitude questions"""
    #normal data
    sm = SignAndMagnitude("dtsm")
    sm.question = -5
    sm.generate_correct_answer()
    assert sm.correct_answer == "10000101"

    sm = SignAndMagnitude("smtd")
    sm.question = "10000101"
    sm.generate_correct_answer()
    assert sm.correct_answer == -5

    sm = SignAndMagnitude("dtsm")
    sm.question = 5
    sm.generate_correct_answer()
    assert sm.correct_answer == "00000101"

    sm = SignAndMagnitude("smtd")
    sm.question = "00000101"
    sm.generate_correct_answer()
    assert sm.correct_answer == 5

    #boundary data
    sm = SignAndMagnitude("smtd")
    sm.question = "00000000"
    sm.generate_correct_answer()
    assert sm.correct_answer == 0

    sm = SignAndMagnitude("smtd")
    sm.question = "10000000"
    sm.generate_correct_answer()
    assert sm.correct_answer == 0

    sm = SignAndMagnitude("dtsm")
    sm.question = 0
    sm.generate_correct_answer()
    assert sm.correct_answer in ["00000000", "10000000"]

    sm = SignAndMagnitude("smtd")
    sm.question = "11111111"
    sm.generate_correct_answer()
    assert sm.correct_answer == -127

    sm = SignAndMagnitude("smtd")
    sm.question = "01111111"
    sm.generate_correct_answer()
    assert sm.correct_answer == 127

def test_twos_complement_generate_question():
    """tests that the generate_question() creates a two's complement question"""
    tc = TwosComplement("dttc")
    tc.generate_question()
    assert isinstance(tc.question, int)
    assert -128 <= tc.question <= 127

    tc = TwosComplement("tctd")
    tc.generate_question()
    assert len(tc.question) == 8
    for digit in tc.question:
        assert digit in ["0", "1"]


def test_twos_complement_generate_correct_answer():
    """tests that the correct answer is generated for two's complement questions"""
    #normal data
    tc = TwosComplement("dttc")
    tc.question = -5
    tc.generate_correct_answer()
    assert tc.correct_answer == "11111011"

    tc = TwosComplement("tctd")
    tc.question = "11111011"
    tc.generate_correct_answer()
    assert tc.correct_answer == -5

    tc = TwosComplement("dttc")
    tc.question = 5
    tc.generate_correct_answer()
    assert tc.correct_answer == "00000101"

    tc = TwosComplement("tctd")
    tc.question = "00000101"
    tc.generate_correct_answer()
    assert tc.correct_answer == 5
    #boundary data
    tc = TwosComplement("tctd")
    tc.question = "00000000"
    tc.generate_correct_answer()
    assert tc.correct_answer == 0

    tc = TwosComplement("tctd")
    tc.question = "10000000"
    tc.generate_correct_answer()
    assert tc.correct_answer == -128

    tc = TwosComplement("tctd")
    tc.question = "01111111"
    tc.generate_correct_answer()
    assert tc.correct_answer == 127


def test_hex_to_dec_generate_question():
    """tests that the generate_question method creates a hexadecimal to decimal question"""
    htd = HexToDec("htd")
    htd.generate_question()
    assert len(htd.question) == 2
    for i in htd.question:
        assert i in "0123456789ABCDEF"

    htd = HexToDec("dth")
    htd.generate_question()
    assert isinstance(htd.question, int)
    assert 0 <= htd.question <= 255


def test_hex_to_dec_generate_correct_answer():
    """tests that the correct answer is generated for hexadecimal to decimal questions"""
    #normal data
    htd = HexToDec("htd")
    htd.question = "E6"
    htd.generate_correct_answer()
    assert htd.correct_answer == 230

    htd = HexToDec("dth")
    htd.question = 230
    htd.generate_correct_answer()
    assert htd.correct_answer == "E6"
    #boundary data-with 0 as the first, last, or both digit
    htd = HexToDec("dth")
    htd.question = 15
    htd.generate_correct_answer()
    assert htd.correct_answer == "0F"

    htd = HexToDec("dth")
    htd.question = 16
    htd.generate_correct_answer()
    assert htd.correct_answer == "10"

    htd = HexToDec("htd")
    htd.question = "00"
    htd.generate_correct_answer()
    assert htd.correct_answer == 0

    htd = HexToDec("dth")
    htd.question = 0
    htd.generate_correct_answer()
    assert htd.correct_answer == "00"


def test_plausible_answers():
    """tests that plausible but wrong answers are generated and added to the list correctly with no duplicates """
    uq = UnsignedQuestion("dtub")
    uq.question = 10
    uq.generate_correct_answer()
    uq.generate_plausible_answers()
    assert len(uq.plausible_answers) == 3
    assert uq.correct_answer in uq.plausible_answers
    assert len(uq.plausible_answers) == len(set(uq.plausible_answers))

    sm = SignAndMagnitude("dtsm")
    sm.question = -5
    sm.generate_correct_answer()
    sm.generate_plausible_answers()
    assert len(sm.plausible_answers) == 3
    assert sm.correct_answer in sm.plausible_answers
    assert len(uq.plausible_answers) == len(set(uq.plausible_answers))

    htd = HexToDec("dth")
    htd.question = 15
    htd.generate_correct_answer()
    htd.generate_plausible_answers()
    assert len(htd.plausible_answers) == 3
    assert htd.correct_answer in htd.plausible_answers
    assert len(uq.plausible_answers) == len(set(uq.plausible_answers))


def test_check_answer():
    """tests if check_answer() verifies users response"""
    uq = UnsignedQuestion("dtub")
    uq.correct_answer = "00010001"
    uq.user_answer = "00010001"
    assert uq.check_answer()

    sm = SignAndMagnitude("dtsm")
    sm.correct_answer = "10100101"
    sm.user_answer = "10100101"
    assert sm.check_answer()

    htd = HexToDec("dth")
    htd.correct_answer = "BA"
    htd.user_answer = "BA"
    assert htd.check_answer()
