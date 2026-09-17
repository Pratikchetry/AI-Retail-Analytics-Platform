-- Human-in-the-Loop review queue
-- Stores any agent answer that exhausted its retry budget while the
-- critic still scored it below the passing threshold. A human can
-- review these later and correct/annotate them.

CREATE TABLE IF NOT EXISTS human_review_queue (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT,
    route TEXT,
    critic_score FLOAT,
    critic_feedback TEXT,
    sql_generated TEXT,
    evidence TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    reviewed BOOLEAN NOT NULL DEFAULT FALSE,
    reviewer_notes TEXT,
    corrected_answer TEXT,
    reviewed_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_review_queue_unreviewed
    ON human_review_queue (reviewed, created_at)
    WHERE reviewed = FALSE;