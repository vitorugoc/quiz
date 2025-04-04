import pytest
from model import Question

@pytest.fixture
def question_with_choices():
    """Fixture que fornece uma questão pré-configurada com 3 choices"""
    question = Question(title="Questão Fixture", points=5)
    question.add_choice("Opção A", False)
    question.add_choice("Opção B", True)
    question.add_choice("Opção C", False)
    return question

@pytest.fixture
def question_with_multiple_correct_choices():
    """Fixture com múltiplas choices corretas"""
    question = Question(title="Questão Múltipla", points=10, max_selections=2)
    question.add_choice("Certa 1", True)
    question.add_choice("Certa 2", True)
    question.add_choice("Errada", False)
    return question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_multiple_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    assert len(question.choices) == 2
    assert question.choices[0].text == 'a'
    assert question.choices[1].text == 'b'

def test_choice_id_incrementation():
    question = Question(title='q1')
    first = question.add_choice('a')
    second = question.add_choice('b')
    assert second.id == first.id + 1

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice = question.add_choice('a')
    question.remove_choice_by_id(choice.id)
    assert len(question.choices) == 0

def test_remove_nonexistent_choice():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.set_correct_choices([c1.id])
    assert c1.is_correct
    assert not c2.is_correct

def test_select_too_many_choices():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a', True)
    c2 = question.add_choice('b', True)
    with pytest.raises(Exception):
        question.select_choices([c1.id, c2.id])

def test_choice_text_validation():
    question = Question(title='q1')
    with pytest.raises(Exception):
        question.add_choice('')
    with pytest.raises(Exception):
        question.add_choice('a'*101)

def test_question_points_validation():
    with pytest.raises(Exception):
        Question(title='q1', points=0)
    with pytest.raises(Exception):
        Question(title='q1', points=101)

def test_select_no_choices_returns_empty_list():
    question = Question(title='q1')
    
    c1 = question.add_choice('Correct 1', True)
    c2 = question.add_choice('Correct 2', True)
    
    result = question.select_choices([])
    
    assert result == []
    assert len(result) == 0

def test_fixture_question_initial_state(question_with_choices):
    """Testa o estado inicial da questão da fixture"""
    assert len(question_with_choices.choices) == 3
    assert question_with_choices.title == "Questão Fixture"
    assert question_with_choices.points == 5

def test_select_correct_choice_with_fixture(question_with_choices):
    """Testa seleção da choice correta usando a fixture"""
    correct_choice = next(c for c in question_with_choices.choices if c.is_correct)
    selected = question_with_choices.select_choices([correct_choice.id])
    assert selected == [correct_choice.id]

def test_remove_choice_with_fixture(question_with_choices):
    """Testa remoção de choice usando a fixture"""
    initial_count = len(question_with_choices.choices)
    choice_to_remove = question_with_choices.choices[0]
    
    question_with_choices.remove_choice_by_id(choice_to_remove.id)
    
    assert len(question_with_choices.choices) == initial_count - 1
    assert choice_to_remove.id not in [c.id for c in question_with_choices.choices]