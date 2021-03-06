# coding: utf-8

from __future__ import unicode_literals

import os
import unittest
import tempfile

import flaskr

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.bd_arq, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.criar_bd()

    def tearDown(self):
        os.close(self.bd_arq)
        os.unlink(flaskr.app.config['DATABASE'])

    def teste_bd_vazio(self):
        res = self.app.get('/')
        self.assertIn(b'nenhuma entrada', res.data)

    def entrar(self, usuario, senha):
        return self.app.post('/entrar', data=dict(
                username=usuario,
                password=senha
            ), follow_redirects=True)

    def teste_login(self):
        rv = self.entrar('admin', 'default')
        self.assertIn(b'Login OK', rv.data)

    def teste_login_invalido(self):
        rv = self.entrar('adminXXX', 'default')
        self.assertIn(b'Usuário inválido', rv.data)
        rv = self.entrar('admin', 'defaultYYY')
        self.assertIn(b'Senha inválida', rv.data)

    def teste_sair(self):
        rv = self.app.get('/sair', follow_redirects=True)
        self.assertIn(b'Logout OK', rv.data)

    def teste_nova_entrada(self):
        self.entrar('admin', 'default')
        rv = self.app.post('/inserir', data=dict(
            titulo='<Olá>',
            texto='<strong>HTML</strong> é permitido aqui'
        ), follow_redirects=True)
        self.assertEquals(rv.status_code, 200)
        self.assertNotIn(b'nenhuma entrada', rv.data)
        self.assertIn(b'&lt;Olá&gt;', rv.data)
        self.assertIn(b'<strong>HTML</strong> é permitido aqui', rv.data)


if __name__ == '__main__':
    unittest.main()
