"""Tests pour le module fp_client"""
import fp_client

def test_scan_returns_dict():
    res = fp_client.scan()
    assert isinstance(res, dict)
    assert 'ok' in res
    assert 'found' in res
    assert 'total' in res

def test_get_account_structure():
    res = fp_client.get_account()
    assert isinstance(res, dict)
    assert 'ok' in res
    if res['ok']:
        assert 'balance' in res
        assert 'currency' in res
    else:
        assert 'error' in res
