INSERT INTO dim_holiday_uk (
    holiday_date,
    holiday_name,
    is_public_holiday,
    holiday_type,
    is_peak_period
)
VALUES
('2009-12-25', 'Christmas Day', TRUE, 'Religious Holiday', TRUE),
('2009-12-26', 'Boxing Day', TRUE, 'National Holiday', TRUE),
('2010-01-01', 'New Year', TRUE, 'National Holiday', FALSE),
('2010-04-02', 'Good Friday', TRUE, 'Religious Holiday', FALSE),
('2010-04-05', 'Easter Monday', TRUE, 'Religious Holiday', FALSE),
('2010-05-03', 'Early May Bank Holiday', TRUE, 'Bank Holiday', FALSE),
('2010-05-31', 'Spring Bank Holiday', TRUE, 'Bank Holiday', FALSE),
('2010-08-30', 'Summer Bank Holiday', TRUE, 'Bank Holiday', FALSE),
('2010-12-25', 'Christmas Day', TRUE, 'Religious Holiday', TRUE),
('2010-12-26', 'Boxing Day', TRUE, 'National Holiday', TRUE),

('2011-01-01', 'New Year', TRUE, 'National Holiday', FALSE),
('2011-04-22', 'Good Friday', TRUE, 'Religious Holiday', FALSE),
('2011-04-25', 'Easter Monday', TRUE, 'Religious Holiday', FALSE),
('2011-05-02', 'Early May Bank Holiday', TRUE, 'Bank Holiday', FALSE),
('2011-05-30', 'Spring Bank Holiday', TRUE, 'Bank Holiday', FALSE),
('2011-08-29', 'Summer Bank Holiday', TRUE, 'Bank Holiday', FALSE),
('2011-12-25', 'Christmas Day', TRUE, 'Religious Holiday', TRUE),
('2011-12-26', 'Boxing Day', TRUE, 'National Holiday', TRUE);