import http from "k6/http";
import { check } from "k6";
import { SharedArray } from "k6/data";
import { Rate } from "k6/metrics";
import { sleep } from "k6";

export const options = {
  "scenarios": {
    "warmup": {
      "executor": "shared-iterations",
      "maxDuration": "30s",
      "iterations": 50,
      "vus": 20,
      "startTime": "0s"
    },
    "loadTest": {
      "executor": "shared-iterations",
      "iterations": 200,
      "vus": 100,
      "startTime": "60s"
    }
  }
};
const errorRate = new Rate("errorRate");
const data = new SharedArray("query", function () {
  // here you can open files, and then do additional processing or generate the array with data dynamically
  const f = JSON.parse(open("./query.json"));
  return f; // f must be an array[]
});

export default function () {
  data.forEach((item, index) => {
    const url = "http://172.17.0.3:5005/search";

    const res = http.post(
      url,
      JSON.stringify({
        vector: (item.embedding).toString(),
        n: 10,
      }),
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    // Check if the request was successful
    check(res, {
      "status is 200": (r) => r.status === 200,
    });

    // Log the result
    console.log(`Request ${index + 1}: ${res.status}`);
  });
}
