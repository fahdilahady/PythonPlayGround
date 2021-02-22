import app

def test_echo():
    web = app.app.test_client()

    rq = web.get('/echo/hello')
    assert rq.status == '405 METHOD NOT ALLOWED' #Only Post Allowed
    assert rq.headers['Content-Type'] == 'application/json'
    assert rq.json ==  {'message':'The method is not allowed for the requested URL.'}


    rq = web.post('/echo/revertThisMessage09') #request Parameterized
    assert rq.status == '200 OK'
    assert rq.headers['Content-Type'] == 'application/json'
    assert rq.json == {'message':'90egasseMsihTtrever'}

    rq = web.post('/echo/ABCDEFGHIJKLMNOPQRSTUWXYZ') #validate len <= 20
    assert rq.status == '400 BAD REQUEST'
    assert rq.headers['Content-Type'] == 'application/json'
    assert rq.json == {'message':'message length cannot exceed 20 chars'}

    rq = web.post('/echo/Abc09@# ') #validate alphanumeric input
    assert rq.status == '400 BAD REQUEST'
    assert rq.headers['Content-Type'] == 'application/json'
    assert rq.json == {'message':'message should contain only alphanumeric characters'}

if __name__ == "__main__":
    test_echo()