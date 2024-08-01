from fast_zero_projeto_final.sanitize import (
    sanitize_case,
    sanitize_nome,
    sanitize_punctuation,
    sanitize_script,
    sanitize_spaces,
)


def test_sanitize_script():
    sanitized = sanitize_script("<script>alert('xss')</script>")

    assert sanitized == "alert('xss')"


def test_sanitize_spaces():
    sanitized = sanitize_spaces('    Manuel        Bandeira Teste ')

    assert sanitized == 'Manuel Bandeira Teste'


def test_sanitize_punctuation():
    sanitized = sanitize_punctuation('Manuel, Bandeira!!!?[]<>;./\\')

    assert sanitized == 'Manuel Bandeira'


def test_sanitize_case():
    sanitized = sanitize_case('ManueL Bandeira AÇÃO')

    assert sanitized == 'manuel bandeira ação'


def test_sanitize_nome():
    sanitized = sanitize_nome('    Manuel        Bandeira !!!')

    assert sanitized == 'manuel bandeira'
