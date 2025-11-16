

 -- NAME transformations

UPDATE personal
SET name = CASE
    WHEN :column='name' AND :technique='masking' THEN
        substr(name, 1, 1) || '**** ' ||
        substr(name, instr(name, ' ') + 1, 1) || '******'

    WHEN :column='name' AND :technique='pseudonymization' THEN
        'user_' || abs(random() % 9000 + 1000)

    WHEN :column='name' AND :technique='tokenization' THEN
        'TKN-' || upper(hex(randomblob(2)))

    ELSE name
END;




 -- DOB transformations

UPDATE personal
SET dob = CASE
    WHEN :column='dob' AND :technique='generalization' THEN
        substr(dob, 4, 2) || '/' || substr(dob, 7, 4)

    WHEN :column='dob' AND :technique='suppression' THEN
        '[HIDDEN]'

    ELSE dob
END;




 -- ADDRESS transformations

UPDATE personal
SET address = CASE
    WHEN :column='address' AND :technique='generalization' THEN
        trim(substr(address, instr(address, ',') + 1))

    WHEN :column='address' AND :technique='suppression' THEN
        '[HIDDEN]'

    ELSE address
END;




-- PHONE transformations
 
UPDATE personal
SET phone = CASE
    WHEN :column='phone' AND :technique='masking' THEN
        substr(phone, 1, 7) || 'XXXXXX'

    WHEN :column='phone' AND :technique='tokenization' THEN
        'PHN-TKN-' || abs(random() % 9000 + 1000)

    ELSE phone
END;




 -- EMAIL transformations
 
UPDATE personal
SET email = CASE
    WHEN :column='email' AND :technique='pseudonymization' THEN
        'user_' || abs(random() % 9000 + 1000) || '@anonmail.com'

    WHEN :column='email' AND :technique='tokenization' THEN
        'TKN-EMAIL-' || abs(random() % 9000 + 1000)

    ELSE email
END;





-- AADHAR
UPDATE personal
SET aadhar = CASE
    WHEN :column='aadhar' AND :technique='tokenization' THEN
        'TKN-' || substr(upper(hex(randomblob(2))), 1, 4)
                || '-' ||
                substr(upper(hex(randomblob(2))), 1, 4)

    WHEN :column='aadhar' AND :technique='hashing' THEN
        'HASH-' || upper(hex(randomblob(16)))

    ELSE aadhar
END;


 -- DRIVER'S LICENSE transformations
 
UPDATE personal
SET drivers_license = CASE
    WHEN :column='drivers_license' AND :technique='masking' THEN
        'DL-' || 'XXXXXX' || substr(drivers_license, -4)

    WHEN :column='drivers_license' AND :technique='tokenization' THEN
        'TKN-DL-' || abs(random() % 9000 + 1000)

    ELSE drivers_license
END;
