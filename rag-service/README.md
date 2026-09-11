Paragraph-aware chunking preserved paragraph boundaries when possible, but long paragraphs still fell back to fixed-size splitting and sometimes broke words or sentences. This motivates recursive boundary-aware splitting.

day12
“Correct retrieval and valid citations do not guarantee a grounded answer. In the evaluation, the pipeline achieved 100% answerability accuracy, citation-ID validity, and expected-source coverage, but only 71.4% manual groundedness because the model repeatedly interpreted a necessary approval condition as sufficient permission. This motivates separate groundedness evaluation rather than relying on retrieval or citation metrics alone.”

run_rag_evals.py results:

Case: reassignment
Question: Can an employee receive a reassigned license before 90 days?
Expected answerable: True
Actual answerable: True
Answerability check: PASS
Citation ID validity: PASS
Citation source coverage: PASS
Answer: Yes, a license may be reassigned before 90 days, but only if the exception is approved by an administrator and recorded in the license audit log.
Citations: ['GUIDE-001:1.0:reassignment:000000-000240', 'GUIDE-001:1.0:reassignment:000200-000440']
Retrieved chunks:
- GUIDE-001:1.0:reassignment:000000-000240 | reassignment | 0.8115
- GUIDE-001:1.0:reassignment:000200-000440 | reassignment | 0.7744
- GUIDE-001:1.0:reassignment:000400-000617 | reassignment | 0.7163
Manual groundedness: (y/n)y

Case: capacity
Question: Does capacity validation automatically purchase more seats?
Expected answerable: True
Actual answerable: True
Answerability check: PASS
Citation ID validity: PASS
Citation source coverage: PASS
Answer: No, capacity validation does not purchase licenses or modify the subscription. The purchasing workflow is separate from the entitlement validation process.
Citations: ['GUIDE-001:1.0:seat-management:000200-000440', 'GUIDE-001:1.0:seat-management:000400-000553']
Retrieved chunks:
- GUIDE-001:1.0:seat-management:000200-000440 | seat-management | 0.7374
- GUIDE-001:1.0:seat-management:000400-000553 | seat-management | 0.7299
- GUIDE-001:1.0:seat-management:000000-000240 | seat-management | 0.6498
Manual groundedness: (y/n)y

Case: trial
Question: Can a trial subscription be renewed?
Expected answerable: True
Actual answerable: True
Answerability check: PASS
Citation ID validity: PASS
Citation source coverage: PASS
Answer: No, trial licenses cannot be extended or renewed under the fictional trial policy.
Citations: ['GUIDE-002:1.0:renewal:000400-000575']
Retrieved chunks:
- GUIDE-002:1.0:renewal:000400-000575 | renewal | 0.7290
- GUIDE-002:1.0:renewal:000000-000240 | renewal | 0.6830
- GUIDE-002:1.0:renewal:000200-000440 | renewal | 0.6603
Manual groundedness: (y/n)y

Case: audit
Question: What information should be recorded in a license audit log?
Expected answerable: True
Actual answerable: True
Answerability check: PASS
Citation ID validity: PASS
Citation source coverage: PASS
Answer: License audit logs must record license assignment, reassignment, and administrative approval events. Each audit record should include the customer, license, action, actor, and timestamp.
Citations: ['GUIDE-001:1.0:audit:000000-000240', 'GUIDE-001:1.0:reassignment:000200-000440']
Retrieved chunks:
- GUIDE-001:1.0:audit:000000-000240 | audit | 0.7535
- GUIDE-001:1.0:audit:000200-000422 | audit | 0.7284
- GUIDE-001:1.0:reassignment:000200-000440 | reassignment | 0.6584
Manual groundedness: (y/n)y

Case: unsupported
Question: What color is the CEO's car?
Expected answerable: False
Actual answerable: False
Answerability check: PASS
Citation ID validity: PASS
Citation source coverage: PASS
Answer: I don't have enough information in the provided sources to answer this question.
Citations: []
Retrieved chunks:
- GUIDE-001:1.0:seat-management:000200-000440 | seat-management | 0.5735
- GUIDE-002:1.0:renewal:000200-000440 | renewal | 0.5706
- GUIDE-002:1.0:renewal:000400-000575 | renewal | 0.5693
Manual groundedness: (y/n)y

Case: exact_cancellation_fee
Question: What is the exact cancellation fee?
Expected answerable: False
Actual answerable: False
Answerability check: PASS
Citation ID validity: PASS
Citation source coverage: PASS
Answer: I don't have enough information in the provided sources to answer this question.
Citations: []
Retrieved chunks:
- GUIDE-002:1.0:cancellation:000000-000240 | cancellation | 0.6787
- GUIDE-002:1.0:cancellation:000200-000440 | cancellation | 0.6441
- GUIDE-002:1.0:cancellation:000400-000478 | cancellation | 0.6426
Manual groundedness: (y/n)y

Case: thirty_day_reassignment
Question: Can I reassign a license after 30 days?
Expected answerable: True
Actual answerable: True
Answerability check: PASS
Citation ID validity: PASS
Citation source coverage: PASS
Answer: A license can be reassigned after 30 days only if you receive administrator approval. Without such approval, the standard policy requires waiting 90 days. Additionally, any approved exceptions to this 90-day rule must be recorded in the license audit log.
Citations: ['GUIDE-001:1.0:reassignment:000000-000240', 'GUIDE-001:1.0:reassignment:000200-000440']
Retrieved chunks:
- GUIDE-001:1.0:reassignment:000000-000240 | reassignment | 0.7909
- GUIDE-001:1.0:reassignment:000200-000440 | reassignment | 0.7429
- GUIDE-002:1.0:cancellation:000400-000478 | cancellation | 0.7069
Manual groundedness: (y/n)n

=== RAG Evaluation Summary === 
Cases: 7
Answerability accuracy: 7 / 7( 1.0)
Citation ID Validity: 1.0 / 7( 1.0)
Citation Expected-Source Coverage: 7 / 7( 1.0)
Manual Groundedness: 6 / 7( 0.9)
Groundedness failures:
- thirty_day_reassignment