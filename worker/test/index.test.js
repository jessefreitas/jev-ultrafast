import test from "node:test";
import assert from "node:assert/strict";
import worker from "../src/index.js";

const request = (body, token = "test-token") => new Request("https://gateway.example/v1/decision", {
  method: "POST",
  headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
  body: JSON.stringify(body),
});

test("rejects a missing gateway token", async () => {
  const response = await worker.fetch(request({}, "wrong"), { JEV_WORKERS_AI_GATEWAY_TOKEN: "test-token" });
  assert.equal(response.status, 401);
});

test("sends only a minimized decision contract to Workers AI", async () => {
  let input;
  const env = {
    JEV_WORKERS_AI_GATEWAY_TOKEN: "test-token",
    AI: { run: async (_model, value) => { input = value; return { response: '{"operation":{"choice":"BLOCKED"}}' }; } },
  };
  const response = await worker.fetch(request({
    state: { text: "Paciente Ana, CPF 12345678901", elements: [{ index: "1", label: "Cliente ana@example.com", operations: ["CLICK"] }] },
    questions: { operation: { type: "choice", criteria: { BLOCKED: "Stop" }, instructions: { goal: "Abra a cliente ana@example.com" } } },
  }), env);
  assert.equal(response.status, 200);
  assert.doesNotMatch(input.messages[1].content, /12345678901|ana@example\.com|Paciente/);
});
