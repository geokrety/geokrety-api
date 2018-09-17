import responses


class ResponsesMixin(object):
    def setUp(self):
        assert responses, 'responses package required to use ResponsesMixin'
        responses.start()
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=43.69448&lon=6.85575',
                      status=200, body='FR', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=43.69448&lon=6.85575',
                      status=200, body='720', match_querystring=True)

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06453&lon=9.32880',
                      status=200, body='DE', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06255&lon=9.34737',
                      status=200, body='DE', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.06313&lon=9.32412',
                      status=200, body='DE', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.07567&lon=9.35367',
                      status=200, body='DE', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.08638&lon=9.50065',
                      status=200, body='DE', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=52.07258&lon=9.35628',
                      status=200, body='DE', match_querystring=True)

        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06453&lon=9.32880',
                      status=200, body='79', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06255&lon=9.34737',
                      status=200, body='73', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.06313&lon=9.32412',
                      status=200, body='84', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.07567&lon=9.35367',
                      status=200, body='126', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.08638&lon=9.50065',
                      status=200, body='130', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=52.07258&lon=9.35628',
                      status=200, body='154', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=0.00000&lon=0.00000',
                      status=200, body='1500', match_querystring=True)

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=42.00000&lon=42.00000',
                      status=400, match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=42.00000&lon=42.00000',
                      status=500, match_querystring=True)

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=None&lon=None',
                      status=500, match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=None&lon=None',
                      status=500, match_querystring=True)

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=43.78000&lon=7.06000',
                      status=200, body='FR', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=43.78000&lon=7.06000',
                      status=200, body='996', match_querystring=True)

        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=0.00000&lon=0.00000',
                      status=200, body='', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=0.00000&lon=0.00000',
                      status=200, body='None', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=0.00000&lon=1.00000',
                      status=200, body='', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=0.00000&lon=1.00000',
                      status=200, body='None', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=1.00000&lon=0.00000',
                      status=200, body='', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=1.00000&lon=0.00000',
                      status=200, body='None', match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=0.00000&lon=None',
                      status=500, match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=0.00000&lon=None',
                      status=500, match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getCountry?lat=None&lon=0.00000',
                      status=500, match_querystring=True)
        responses.add(responses.GET, 'https://geo.kumy.org/api/getElevation?lat=None&lon=0.00000',
                      status=500, match_querystring=True)

        super(ResponsesMixin, self).setUp()

    def tearDown(self):
        super(ResponsesMixin, self).tearDown()
        responses.stop()
        responses.reset()
