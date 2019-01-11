set search_path to home_loans, meta;

---------------------------------------------------------------------------------
--------------------------- Create Home Loan Functions --------------------------
---------------------------------------------------------------------------------


-- Called by the _pricing_filter_view

create or replace function pricing_discount(p_request_id integer, p_loan_id integer)
returns numeric(5,2) as
$$
declare
    discount numeric(5,2);
begin
    select D.rate
    into discount
    from
             home_loans.request      R,
             home_loans.loan         L
        join home_loans.discount     D    using (loan_id)
        join home_loans.lvr_range    DL   using (lvr_range_id)
        join home_loans.amount_range DA   using (amount_range_id)
    where
            R.request_id = p_request_id
        and L.loan_id = p_loan_id
        and L.has_value_discounts is true
        and R.lvr    between DL.min_lvr    and DL.max_lvr
        and R.amount between DA.min_amount and DA.max_amount;

    return coalesce(discount,0.0);

end;
$$ language 'plpgsql';

    ------------------------------------------------------------------

-- Called by the _pricing_filter_view

create or replace function postcode_discount(p_request_id integer, p_loan_id integer)
returns numeric(5,2) as
$$
declare
    discount numeric(5,2);
begin
    select L.postcode_discount
    into discount
    from
        home_loans.request   R,
        home_loans.loan      L,
        meta.postcode_list_member P
    where
            R.request_id = p_request_id
        and L.loan_id = p_loan_id
        and L.has_postcode_discount
        and L.postcode_discount_list_id = P.postcode_list_id
        and R.postcode = P.postcode;

    return coalesce(discount,0.0);
end;
$$ language 'plpgsql';

    ------------------------------------------------------------------

-- Called by the _pricing_filter_view

create or replace function pricing_cashback(p_request_id integer, p_loan_id integer)
returns integer as
$$
declare
    cashback integer;
begin
    select
        cast (
            case
                when L.cashback_is_a_rate
                    then ( L.cashback * R.amount ) / 100000
                else L.cashback
            end
            as integer
        )
    into cashback
    from
        home_loans.request   R,
        home_loans.loan      L
    where
            R.request_id = p_request_id
        and L.loan_id = p_loan_id
        and L.has_cashback
        and L.cashback > 0;

    return coalesce(cashback, 0);
end;
$$ language 'plpgsql';

    ------------------------------------------------------------------
