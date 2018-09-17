import responses


class ResponsesMixin(object):
    def setUp(self):
        assert responses, 'responses package required to use ResponsesMixin'
        responses.start()
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=43.69448&lon=6.85575',
                      status=200, body='FR')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=43.69448&lon=6.85575',
                      status=200, body='720')

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06453&lon=9.32880',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06255&lon=9.34737',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06313&lon=9.32412',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.07567&lon=9.35367',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.08638&lon=9.50065',
                      status=200, body='DE')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.07258&lon=9.35628',
                      status=200, body='DE')

        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06453&lon=9.32880',
                      status=200, body='79')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06255&lon=9.34737',
                      status=200, body='73')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06313&lon=9.32412',
                      status=200, body='84')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.07567&lon=9.35367',
                      status=200, body='126')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.08638&lon=9.50065',
                      status=200, body='130')
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.07258&lon=9.35628',
                      status=200, body='154')

        super(ResponsesMixin, self).setUp()

    def tearDown(self):
        super(ResponsesMixin, self).tearDown()
        responses.stop()
        responses.reset()
