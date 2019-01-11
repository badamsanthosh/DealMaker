set search_path to home_loans;

-- Purge All exiting Views to reload them:
drop view if exists similar_view;
drop view if exists email_view;
drop view if exists quoting_quote_view;
drop view if exists lead_view;
drop view if exists price_smsf_request_view;
drop view if exists price_request_view;
drop view if exists _request_all_view;
drop view if exists _pricing_filter_view;

------------------------------------------------------------------------------
-------------------------- Create Home Loan Views ----------------------------
------------------------------------------------------------------------------

-- View to display similar leads information

create or replace view similar_view as
    select
        R1.request_id,
        R2.request_id as similar_request_id,
        R2.created_on,
        R2.first_name,
        R2.last_name,
        R2.phone,
        R2.email,
        R2.amount
    from request R1, request R2
    where
        R1.request_id != R2.request_id and
        not R2.discarded and
        (
            R1.phone = R2.phone or
            R1.email = R2.email or
            lower(R1.first_name || R1.last_name) = lower(R2.first_name || R2.last_name)
        );

    ------------------------------------------------------------------

-- Used by price_request_view
    -- Pre-Requisites: Create below functions
        -- pricing_discount
        -- postcode_discount
        -- pricing_cashback

create or replace view _pricing_filter_view as
    select
        request_id,
        loan_id,
        pricing_discount(request_id, loan_id)  as pricing_discount,
        postcode_discount(request_id, loan_id) as postcode_discount,
        pricing_cashback(request_id, loan_id)  as pricing_cashback
    from
        request                        R,
        loan                           L
        join applies_to_reason         LR  using(loan_id)
        join applies_to_state          LS  using(loan_id)
        join applies_to_property_type  LP  using(loan_id)
    where
            L.is_current
        and
            L.is_attached
        and
            R.channel_path = L.channel_path
        and
            R.reason = LR.reason
        and
            R.state  = LS.state
        and
            R.property_type = LP.property_type
        and
            (R.amount between L.min_amount and L.max_amount)
        and
            R.lvr <= L.max_lvr
        and
        (
            L.postcode_exclusion_list_id is null or
            R.postcode not in (
                select postcode from meta.postcode_list_member
                where postcode_list_id = L.postcode_exclusion_list_id
            )
        )
        and
        (
            (R.show_fixed    and L.rate_type = 'fixed'   ) or
            (R.show_variable and L.rate_type = 'variable')
        )
        and
        (
                -- ignore serviceblility over $250K
                R.disposable_income > 4330 or

                -- (((amount * (rate / 100) / 12) / disposable_income) * 100 < 130
                -- which simplifies to ...
                ( R.amount * L.rate ) / ( 12 * R.disposable_income ) < 130
        );

        ------------------------------------------------------------------

-- Used By :
    -- Get price Request API

create or replace view price_request_view as
    select distinct
        F.request_id,   -- key for search
        F.loan_id,
        L.brand_path,
        L.rate_type,
        L.rate - F.pricing_discount - F.postcode_discount as rate,
        F.pricing_cashback as cashback
    from
        _pricing_filter_view F
        join loan            L using(loan_id)
    where
           F.pricing_cashback  > 0
        or F.pricing_discount  > 0
        or F.postcode_discount > 0;

        ------------------------------------------------------------------

-- Used By :
    -- Get price request for SMSF

-- TODO:
    -- See if this can be merged into single pricing request view.

create or replace view price_smsf_request_view as
    select
        AP.request_id,   -- key for search
        AP.loan_id,
        AP.brand_path,
        AP.rate_type,
        AP.rate,
        AP.cashback
    from
        price_request_view AP
        join loan           L using(loan_id)
        join request        R using(request_id)
    where
       (R.trustee_is_a_company or not L.trustee_must_be_a_company) and
       R.trust_balance >= L.min_trust_balance;

       ------------------------------------------------------------------

-- Used By :
    -- Get Quotes Count

-- Notes:
    -- If a service call is duplicated in a very short period of time, say, from
    -- separate processes, quotes may be generated twice. In this case, we only
    -- want to return the first of the duplicated quotes.
-- set search_path to public;

-- If a service call is duplicated in a very short period of time, say, from
-- separate processes, quotes may be generated twice. In this case, we only
-- want to return the first of the duplicated quotes.

create or replace view quote_view as
    select
        quote_id,
        request_id,

        Q.rate,
        Q.cashback,
        Q.p_and_i_estimate,
        Q.io_estimate,

        L.brand_path,
        L.brand_name,

        L.display_name as name,
        L.description,

        L.is_honeymoon,
        L.rate as advertised_rate,
        L.rate_type,
        L.fixed_term,
        L.max_term,
        L.max_lvr,
        L.min_amount,
        L.max_amount,

        L.has_offset,
        L.has_redraw,
        L.has_extra_payments,
        L.has_extra_payment_penalty,
        L.has_interest_only,
        array_to_string(L.frequencies,',') as frequencies,
        L.application_fee,
        L.monthly_fee,
        L.annual_fee,

        L.max_rent_towards_repayment,
        L.max_super_towards_repayment

    from quote    Q
    join loan     L using(loan_id)
    join request  R using(request_id)
    WHERE Q.is_current='true';

       ------------------------------------------------------------------
