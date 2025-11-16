-- ============================================================
-- Financial Data Anonymizer (SQLite-Safe)
-- Applies CASE-based anonymization depending on technique
-- Input table must be named: financial
-- ============================================================

DROP TABLE IF EXISTS anonymized_data;

CREATE TABLE anonymized_data AS
SELECT
    ----------------------------------------------------------
    -- 1. CARD NUMBER (Masking / Tokenization)
    ----------------------------------------------------------
    CASE
        WHEN 'card_number' = :column AND 'masking' = :technique
            THEN 'XXXX-XXXX-XXXX-' || SUBSTR(card_number, -4)
        WHEN 'card_number' = :column AND 'tokenization' = :technique
            THEN 'TKN-CC-' || UPPER(SUBSTR(HEX(card_number), 1, 4))
        ELSE card_number
    END AS card_number,

    ----------------------------------------------------------
    -- 2. BANK ACCOUNT (Masking / Tokenization)
    ----------------------------------------------------------
    CASE
        WHEN 'bank_account' = :column AND 'masking' = :technique
            THEN 'XXXXXX' || SUBSTR(bank_account, -4)
        WHEN 'bank_account' = :column AND 'tokenization' = :technique
            THEN 'ACC-TKN-' || SUBSTR(ABS(RANDOM()), 1, 4)
        ELSE bank_account
    END AS bank_account,

    ----------------------------------------------------------
    -- 3. TRANSACTION AMOUNT (Perturbation / Differential Privacy)
    ----------------------------------------------------------
    CASE
        WHEN 'transaction_amount' = :column AND 'perturbation' = :technique
            THEN transaction_amount + (ABS(RANDOM()) % 50 - 25)
        ELSE transaction_amount
    END AS transaction_amount,

    ----------------------------------------------------------
    -- 4. SALARY (Generalization / Perturbation)
    ----------------------------------------------------------
    CASE
        WHEN 'salary' = :column AND 'generalization' = :technique
            THEN 
                CASE 
                    WHEN salary < 300000 THEN '0–3L'
                    WHEN salary < 500000 THEN '3–5L'
                    WHEN salary < 700000 THEN '5–7L'
                    WHEN salary < 900000 THEN '7–9L'
                    ELSE '9L+'
                END
        WHEN 'salary' = :column AND 'perturbation' = :technique
            THEN salary + (ABS(RANDOM()) % 5000 - 2500)
        ELSE salary
    END AS salary,

    ----------------------------------------------------------
    -- 5. PAN Number (Tokenization / Hashing)
    ----------------------------------------------------------
    CASE
        WHEN 'pan' = :column AND 'tokenization' = :technique
            THEN 'TKN-PAN-' || SUBSTR(ABS(RANDOM()), 1, 4)
        WHEN 'pan' = :column AND 'hashing' = :technique
            THEN 'HASH_' || SUBSTR(HEX(pan), 1, 8)
        ELSE pan
    END AS pan

FROM financial;

-- Replace original table with anonymized table
DROP TABLE IF EXISTS financial;
ALTER TABLE anonymized_data RENAME TO financial;
