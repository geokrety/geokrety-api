import factory

# use camelCase for naming variables

string_ = 'example'
email_ = factory.Sequence(lambda n: 'user{0}@example.com'.format(n))
integer_ = 25
url_ = 'http://example.com'
imageUrl_ = 'https://www.w3schools.com/html/pic_mountain.jpg'
date_time_ = '2016-12-13 23:59:59'
date_ = '2016-12-14'
country_ = 'US'
int_ = '1'
float_ = '1.23456789'
timezone_ = 'UTC'
environment_ = 'production'
ip_ = '172.16.1.1'
