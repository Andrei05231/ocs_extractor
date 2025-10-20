-- If the ocs database is updated while no user is logged in, don t update the user

DELIMITER $$

CREATE TRIGGER hardware_userid_sticky
BEFORE UPDATE ON hardware
FOR EACH ROW
BEGIN
    IF NEW.USERID IS NULL OR NEW.USERID = '' THEN
        SET NEW.USERID = OLD.USERID;
    END IF;
END$$

DELIMITER ;
