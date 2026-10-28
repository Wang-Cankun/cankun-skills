/**
 * Structured-result tool for fleet-job Pi workers.
 *
 * Loaded with `pi -e submit_result.ts` when a job has a schema. Reads the JSON Schema
 * from FLEET_JOB_SCHEMA and registers `submit_result` with it as the parameter schema, so
 * Pi validates the model's submission and returns validation errors for a retry. If the
 * run completes without a submission, it appends a reminder and continues (twice at most).
 */
import { readFileSync } from "node:fs";

const MAX_REMINDERS = 2;

export default function (pi: any) {
	const schemaPath = process.env.FLEET_JOB_SCHEMA;
	if (!schemaPath) return;
	const schema = JSON.parse(readFileSync(schemaPath, "utf8"));

	let submitted = false;
	let reminders = 0;

	pi.registerTool({
		name: "submit_result",
		label: "Submit Result",
		description:
			"Submit your final result as structured data matching this tool's parameter schema. Call it exactly once, as your last action.",
		promptSnippet: "Submit the final structured result",
		promptGuidelines: [
			"When the task is complete, call submit_result exactly once with the final result; do not answer in prose afterwards.",
			"If submit_result reports a validation error, correct the arguments and call it again.",
		],
		parameters: schema,
		async execute(_toolCallId: string, params: unknown) {
			submitted = true;
			return {
				content: [{ type: "text", text: "Result recorded." }],
				details: params,
				terminate: true,
			};
		},
	});

	pi.on("agent_before_settle", async (event: any) => {
		// Only remind after a normal completion; never re-request after an API error or abort.
		if (submitted || reminders >= MAX_REMINDERS || event.outcome !== "completed") return;
		reminders++;
		return {
			continue: true,
			entries: [
				{
					type: "custom_message",
					customType: "pi-job-reminder",
					content: "You have not called submit_result. Call submit_result now with your final result.",
					display: false,
				},
			],
		};
	});
}
