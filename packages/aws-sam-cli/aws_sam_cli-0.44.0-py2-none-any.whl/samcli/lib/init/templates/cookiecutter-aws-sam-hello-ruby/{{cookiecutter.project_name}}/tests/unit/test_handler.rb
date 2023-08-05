require 'json'
require 'test/unit'
require 'mocha/test_unit'

require_relative '../../hello_world/app'

class HelloWorldTest < Test::Unit::TestCase
  def event
    {
      body: 'eyJ0ZXN0IjoiYm9keSJ9',
      resource: '/{proxy+}',
      path: '/path/to/resource',
      httpMethod: 'POST',
      isBase64Encoded: true,
      queryStringParameters: {
        foo: 'bar'
      },
      pathParameters: {
        proxy: '/path/to/resource'
      },
      stageVariables: {
        baz: 'qux'
      },
      headers: {
        'Accept' => 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' => 'gzip, deflate, sdch',
        'Accept-Language' => 'en-US,en;q=0.8',
        'Cache-Control' => 'max-age=0',
        'CloudFront-Forwarded-Proto' => 'https',
        'CloudFront-Is-Desktop-Viewer' => 'true',
        'CloudFront-Is-Mobile-Viewer' => 'false',
        'CloudFront-Is-SmartTV-Viewer' => 'false',
        'CloudFront-Is-Tablet-Viewer' => 'false',
        'CloudFront-Viewer-Country' => 'US',
        'Host' => '1234567890.execute-api.us-east-1.amazonaws.com',
        'Upgrade-Insecure-Requests' => '1',
        'User-Agent' => 'Custom User Agent String',
        'Via' => '1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)',
        'X-Amz-Cf-Id' => 'cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==',
        'X-Forwarded-For' => '127.0.0.1, 127.0.0.2',
        'X-Forwarded-Port' => '443',
        'X-Forwarded-Proto' => 'https'
      },
      requestContext: {
        accountId: '123456789012',
        resourceId: '123456',
        stage: 'prod',
        requestId: 'c6af9ac6-7b61-11e6-9a41-93e8deadbeef',
        requestTime: '09/Apr/2015:12:34:56 +0000',
        requestTimeEpoch: 1428582896000,
        identity: {
          cognitoIdentityPoolId: 'null',
          accountId: 'null',
          cognitoIdentityId: 'null',
          caller: 'null',
          accessKey: 'null',
          sourceIp: '127.0.0.1',
          cognitoAuthenticationType: 'null',
          cognitoAuthenticationProvider: 'null',
          userArn: 'null',
          userAgent: 'Custom User Agent String',
          user: 'null'
        },
        path: '/prod/path/to/resource',
        resourcePath: '/{proxy+}',
        httpMethod: 'POST',
        apiId: '1234567890',
        protocol: 'HTTP/1.1'
      }
    }
  end

  def mock_response
    Object.new.tap do |mock|
      mock.expects(:code).returns(200)
      mock.expects(:body).returns('1.1.1.1')
    end
  end

  def expected_result
    {
      statusCode: 200,
      body: {
        message: 'Hello World!',
        location: '1.1.1.1'
      }.to_json
    }
  end

  def test_lambda_handler
    HTTParty.expects(:get).with('http://checkip.amazonaws.com/').returns(mock_response)
    assert_equal(lambda_handler(event: event, context: ''), expected_result)
  end
end
