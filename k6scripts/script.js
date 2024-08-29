import http from 'k6/http';
import { sleep } from 'k6';

// Run load with 2 virtual users for 1 minute
export const options = {
  vus: 2,
  duration: '1m',
};

// Send a GET to https://test.k6.io then sleep for 1s
// before repeating the function (ie. sending another request)
export default function () {
  http.get('https://test.k6.io');
  sleep(1);
}

export function teardown() {
  let post_params = {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Api-Token ${__ENV.K6_DYNATRACE_APITOKEN}`
    },
  };

  // Send SDLC event at the end of the test
  let payload = {
    "event.provider": "k6",
    "event.type": "test",
    "event.category": "finished",
    "service": "dummyservice",
    "duration": options.duration
  }
  let res = http.post(`${__ENV.K6_DYNATRACE_URL}/platform/ingest/v1/events.sdlc`, JSON.stringify(payload), post_params);
}