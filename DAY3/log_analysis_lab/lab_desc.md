 
Extracting Error Patterns from Application Logs Using AI
Objective: To use GitHub Copilot Chat to summarize an application log, extract recurring error patterns with structured prompts, and validate the AI's findings against the raw log lines.
Prerequisites:
•  Visual Studio Code with GitHub Copilot signed in (Coding module, Demo 01)
 
Steps to be followed:
1.  Set up the application log
2.  Summarize the log using Ask mode
3.  Group and count the errors with a structured prompt
4.  Query the error pattern in more detail
5.  Validate the AI's findings against the raw log
 
Step 1: Set up the application log
1.  Open Visual Studio Code. Select File > Open Folder, create a new folder named log_analysis_lab, and open it
2.  Use the bundled [app.log](./app.log) (or create it with the following content). It is a slice of the alert explainer API's log from an overnight window:
app.log
2026-09-10 02:14:01 INFO  [alerts-api] Application startup complete
2026-09-10 02:15:33 INFO  [alerts-api] POST /alerts/ 201 12ms
2026-09-10 02:17:02 INFO  [alerts-api] POST /alerts/1/explain 200 45ms
2026-09-10 02:22:18 ERROR [alerts-api] POST /alerts/2/explain 500 -- AttributeError: 'NoneType' object has no attribute 'upper'
2026-09-10 02:22:19 INFO  [alerts-api] Retrying request 2/3
2026-09-10 02:31:47 INFO  [alerts-api] POST /alerts/3/explain 200 51ms
2026-09-10 02:44:09 ERROR [alerts-api] POST /alerts/7/explain 500 -- AttributeError: 'NoneType' object has no attribute 'upper'
2026-09-10 02:44:10 INFO  [alerts-api] Retrying request 2/3
2026-09-10 02:58:22 WARN  [alerts-api] Database connection pool at 82% capacity
2026-09-10 03:05:41 INFO  [alerts-api] POST /alerts/9/explain 200 48ms
2026-09-10 03:12:56 ERROR [alerts-api] POST /alerts/11/explain 500 -- AttributeError: 'NoneType' object has no attribute 'upper'
2026-09-10 03:12:57 INFO  [alerts-api] Retrying request 2/3
2026-09-10 03:20:03 ERROR [alerts-api] GET /alerts/14 404 -- Alert not found
2026-09-10 03:33:19 INFO  [alerts-api] POST /alerts/15/explain 200 44ms
2026-09-10 03:41:52 ERROR [alerts-api] POST /alerts/18/explain 500 -- AttributeError: 'NoneType' object has no attribute 'upper'
2026-09-10 03:41:53 INFO  [alerts-api] Retrying request 2/3
2026-09-10 03:50:07 WARN  [alerts-api] Database connection pool at 91% capacity
2026-09-10 04:02:31 ERROR [alerts-api] POST /alerts/21/explain 500 -- AttributeError: 'NoneType' object has no attribute 'upper'
2026-09-10 04:02:32 INFO  [alerts-api] Retrying request 2/3
2026-09-10 04:15:44 INFO  [alerts-api] POST /alerts/23/explain 200 47ms

 
Step 2: Summarize the log using Ask mode
1.  Press Ctrl+Alt+I to open the Copilot Chat view, select Ask mode, and enter the following prompt. The #file reference attaches the log, so you do not need to paste its contents:
Prompt (Ask mode)
#file:app.log is a slice of our application log from last night. Summarize what happened, in chronological order, in plain language. Call out anything abnormal.



 
Expected result: The service started normally and handled several successful /explain requests, but from 02:22 it repeatedly returned a 500 error on /explain with an AttributeError on a NoneType. The database connection pool was flagged twice as approaching capacity, and there was one 404 for an alert that does not exist.
**Worked example (compare with your Ask-mode response):**

The API started normally at 02:14:01, created an alert, and successfully explained alert 1. Starting at 02:22:18, five explain requests returned HTTP 500 because `.upper()` was attempted on `None`. Successful explain requests continued between failures. The database connection pool reached 82% at 02:58:22 and 91% at 03:50:07. In between, a request for alert 14 returned HTTP 404. The last 500 was at 04:02:31; the final log entry was a successful explain request at 04:15:44.
 



 
Step 3: Group and count the errors with a structured prompt
1.  In the same chat (Ask mode), enter the following prompt:
Prompt (Ask mode)
From #file:app.log, group ERROR and WARN lines by message pattern in a table with the columns Level, Message, Count, First seen, Last seen, and Endpoint. Group repeated failures on the same route when only the alert ID differs. Group database connection pool warnings even if their capacity percentages differ, and report both percentages.



 
 
Expected result: AttributeError: 5 occurrences on POST /alerts/{id}/explain, first at 02:22:18 and last at 04:02:31; 404 Alert not found: 1 occurrence on GET /alerts/14 at 03:20:03; database connection pool warning: 2 occurrences, at 02:58:22 and 03:50:07.
**Worked example (compare with your Ask-mode response):**

| Level | Message | Count | First seen | Last seen | Endpoint |
|---|---|---:|---|---|---|
| ERROR | HTTP 500: `AttributeError: 'NoneType' object has no attribute 'upper'` | 5 | 02:22:18 | 04:02:31 | `POST /alerts/{id}/explain` |
| ERROR | HTTP 404: Alert not found | 1 | 03:20:03 | 03:20:03 | `GET /alerts/14` |
| WARN | Database connection pool at 82% and 91% capacity | 2 | 02:58:22 | 03:50:07 | Not logged |

 
Note: A structured prompt that names the exact columns you need turns a long log into a table you can act on and compare across runs.
 
Step 4: Query the error pattern in more detail
1.  Enter the following prompt to examine the recurring error:
Prompt (Ask mode)
For the AttributeError in #file:app.log, list the affected alert IDs and the timestamp of any retry message immediately after each failure. Say whether the retries' outcomes are logged and whether the log contains evidence that the database connection pool warnings caused these errors. Answer only from what is in the log.



 
Expected result: The affected alert IDs are 2, 7, 11, 18, and 21, and each failure is followed by a Retrying request 2/3 line. The log shows no evidence that the pool warnings caused the errors: the first error occurs before the first warning, and the error message points to a None value in the code, not to the database.
**Worked example (compare with your Ask-mode response):**

| Alert ID | Failure time | Time of next `Retrying request 2/3` line | Raw log lines |
|---|---|---|---|
| 2 | 02:22:18 | 02:22:19 | 4-5 |
| 7 | 02:44:09 | 02:44:10 | 7-8 |
| 11 | 03:12:56 | 03:12:57 | 11-12 |
| 18 | 03:41:52 | 03:41:53 | 15-16 |
| 21 | 04:02:31 | 04:02:32 | 18-19 |

Each failure is immediately followed by a retry message one second later. The retry messages do not include an alert ID or an outcome, so the log does not confirm whether any retry succeeded. The first 500 predates the first pool warning, and no line links the warnings to the failures. The exception shows that `.upper()` was attempted on `None`, but the log does not identify which value was `None` or why.

 
Note: If Copilot suggests a cause that the log does not support, such as database load, treat it as a hypothesis to investigate, not as a finding.
Step 5: Validate the AI's findings against the raw log
1.  Select Terminal > New Terminal and run the following PowerShell commands to count the patterns independently:
PowerShell
@(Select-String -Path .\app.log -Pattern "AttributeError: 'NoneType' object has no attribute 'upper'" -SimpleMatch).Count
@(Select-String -Path .\app.log -Pattern "404 -- Alert not found" -SimpleMatch).Count
@(Select-String -Path .\app.log -Pattern " WARN " -SimpleMatch).Count

 
Expected result: The commands return 5, 1, and 2, matching the counts that Copilot reported in Step 3. If a count differs, tell Copilot which lines it missed.
**Linux/macOS alternative:** Run from the lab folder if PowerShell is unavailable.

```bash
grep -cF "AttributeError: 'NoneType' object has no attribute 'upper'" app.log
grep -cF '404 -- Alert not found' app.log
grep -cF ' WARN ' app.log
```

**Verified output (`grep`):**

```text
5
1
2
```
 

 
2.  Note the conclusion for the next lab: the recurring AttributeError on the /explain endpoint is the issue to escalate. The applied lab (Demo 03) reproduces this same failure in the capstone project and fixes it.
**Validation checklist for the worked examples**

| Check | Expected result | Status |
|---|---|---|
| Log summary | Recurring HTTP 500 / AttributeError starts at 02:22:18 | Pass |
| Structured count | 5 AttributeErrors, 1 HTTP 404, and 2 pool warnings, with first and last timestamps | Pass |
| Pattern query | IDs 2, 7, 11, 18, and 21; each followed by a retry message; no evidence that the pool warnings caused the errors | Pass |
| Manual validation | Independent fixed-string counts of 5, 1, and 2 | Pass (`grep`; PowerShell not run) |
 

 
Why this matters: A production log with thousands of lines is not read top to bottom. AI-assisted log analysis turns it into a short summary and a table that point to what to investigate next, but the counts and any suggested causes must be checked against the raw log before they drive a decision.
By following these steps, you have successfully used GitHub Copilot Chat to summarize an application log, extract and query recurring error patterns with structured prompts, and validate the findings against the raw log.
