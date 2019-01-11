set search_path to public, home_loans, lending;

-- Insert Demo Brand
INSERT INTO lending.brand (brand_path, name, is_active, created_on, updated_on) values ('cba', 'CBA', true, now(), now());
INSERT INTO lending.brand (brand_path, name, is_active, created_on, updated_on) values ('bom', 'Bank of Melbourne', true, now(), now());
INSERT INTO lending.brand (brand_path, name, is_active, created_on, updated_on) values ('nab', 'National Australian Bank', true, now(), now());
--------------------------------------------------------------------------------
-- Insert Home Loans Data
INSERT into home_loans.loan (
    loan_id,
    is_attached,
    is_current,
    owner_id,
    channel_path,
    brand_path,
    product_name,
    description,
    min_amount,
    max_amount,
    max_lvr,
    rate_type,
    rate,
    cashback,
    cashback_is_a_rate,
    has_value_discounts,
    has_postcode_discount,
    has_cashback,
    cashback_legal,
    is_honeymoon,
    postcode_discount_list_id,
    postcode_discount,
    max_term,
    created_on,
    updated_on
)
values (
    1,          -- loan_id,
    true,       -- is_attached
    true,       -- is_current
    1,          -- owner_id,
    'personal', -- channel_path
    'cba',      -- brand_path
    'Test',     -- product_name,
    'Test Desc',-- description
    10000,      -- min_amount,
    1000000,    -- max_amount,
    95,         -- max_lvr,
    'fixed',    -- rate_type,
    5.00,       -- rate,
    null,       -- cashback,
    false,      -- cashback_is_a_rate,
    false,      -- has_value_discounts,
    false,      -- has_postcode_discount,
    false,      -- has_cashback,
    true,       -- cashback_legal,
    false,      -- is_honeymoon,
    null,       -- postcode_list_id,
    null,       -- postcode_discount,
    25,         -- max_term,
    now(),      -- Created On,
    now()       -- Updated On
);
----------------------------------------
INSERT into home_loans.loan (
    loan_id,
    is_attached,
    is_current,
    owner_id,
    channel_path,
    brand_path,
    product_name,
    description,
    min_amount,
    max_amount,
    max_lvr,
    rate_type,
    rate,
    cashback,
    cashback_is_a_rate,
    has_value_discounts,
    has_postcode_discount,
    has_cashback,
    cashback_legal,
    is_honeymoon,
    postcode_discount_list_id,
    postcode_discount,
    max_term,
    created_on,
    updated_on
)
values (
    2,          -- loan_id,
    true,       -- is_attached
    true,       -- is_current
    1,          -- owner_id,
    'personal', -- channel_path
    'nab',      -- brand_path
    'Simply Loan',     -- product_name,
    'Best Loan',-- description
    5000,      -- min_amount,
    5000000,    -- max_amount,
    95,         -- max_lvr,
    'fixed',    -- rate_type,
    3.45,       -- rate,
    null,       -- cashback,
    false,      -- cashback_is_a_rate,
    false,      -- has_value_discounts,
    false,      -- has_postcode_discount,
    false,      -- has_cashback,
    true,       -- cashback_legal,
    false,      -- is_honeymoon,
    null,       -- postcode_list_id,
    null,       -- postcode_discount,
    30,         -- max_term,
    now(),      -- Created On,
    now()       -- Updated On
);
--------------------------------------------------------------------------------

INSERT INTO home_loans.applies_to_reason(reason, loan_id, created_on, updated_on) values ('buying', 1, now(), now());
INSERT INTO home_loans.applies_to_reason(reason, loan_id, created_on, updated_on) values ('refinance', 1, now(), now());
INSERT INTO home_loans.applies_to_reason(reason, loan_id, created_on, updated_on) values ('buying', 2, now(), now());
INSERT INTO home_loans.applies_to_reason(reason, loan_id, created_on, updated_on) values ('refinance', 2, now(), now());

INSERT into home_loans.applies_to_state(loan_id, state, created_on, updated_on) values ( 1, 'VIC', now(), now());
INSERT into home_loans.applies_to_state(loan_id, state, created_on, updated_on) values ( 1, 'NSW', now(), now());
INSERT into home_loans.applies_to_state(loan_id, state, created_on, updated_on) values ( 1, 'QLD', now(), now());

INSERT INTO home_loans.applies_to_property_type(loan_id, property_type, created_on, updated_on) values ( 1, 'house', now(), now());
INSERT INTO home_loans.applies_to_property_type(loan_id, property_type, created_on, updated_on) values ( 1, 'apartment', now(), now());

--------------------------------------------------------------------------------

INSERT  INTO home_loans.amount_range(loan_id, min_amount, max_amount, created_on, updated_on) values (1, 500001,600000, now(), now());
INSERT  INTO home_loans.amount_range(loan_id, min_amount, max_amount, created_on, updated_on) values (1, 600001,700000, now(), now());
INSERT  INTO home_loans.amount_range(loan_id, min_amount, max_amount, created_on, updated_on) values (1, 700001,800000, now(), now());

INSERT  INTO home_loans.lvr_range(loan_id, min_amount, max_amount, created_on, updated_on) values (1, 0, 80, now(), now());
INSERT  INTO home_loans.lvr_range(loan_id, min_amount, max_amount, created_on, updated_on) values (1, 81, 90, now(), now());
INSERT  INTO home_loans.lvr_range(loan_id, min_amount, max_amount, created_on, updated_on) values (1, 91, 100, now(), now());

INSERT  INTO home_loans.discount(loan_id, lvr_range_id, amount_range_id, rate, created_on, updated_on) values (1, 1, 1, 1.10, now(), now());
INSERT  INTO home_loans.discount(loan_id, lvr_range_id, amount_range_id, rate, created_on, updated_on) values (1, 1, 2, 1.20, now(), now());
INSERT  INTO home_loans.discount(loan_id, lvr_range_id, amount_range_id, rate, created_on, updated_on) values (1, 1, 3, 1.30, now(), now());

--------------------------------------------------------------------------------

-- Insert data into Home Loan Request

INSERT INTO home_loans.request (
    channel_path,
    state,
    postcode,
    amount,
    price,
    lvr,
    disposable_income,
    show_fixed,
    show_variable,
    reason,
    property_type,
    trustee_is_a_company,
    trust_balance,
    discarded,
    created_on,
    updated_on
)
VALUES (
    'personal', -- channel_path,
    'VIC',      -- state,                   matches state
    '3000',     -- postcode,
    500000,     -- amount,                  between 100,000 and 1,000,000
    600000,     -- price,
    83,         -- lvr,                     < 95
    2025.00,    -- disposable_income,       servicable
    true,       -- show_fixed,
    true,       -- show_variable,
    'buying',   -- reason,                  matches reason
    'house',    -- property_type,           matches property_type
    null,       -- trustee_is_a_company,
    null,       -- trust_balance,
    'f',        -- Discarded,
    now(),      -- Created On,
    now()       -- Updated On
);

----------------------------------------


