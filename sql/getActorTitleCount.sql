DELIMITER $$
CREATE DEFINER=`root`@`%` FUNCTION `getActorTitleCount`(p_personId VARCHAR(12)) RETURNS int
    READS SQL DATA
BEGIN
	DECLARE count INT;
    SET count = 0;
    
	SELECT COUNT(DISTINCT(movShowId)) INTO count FROM Roles WHERE Roles.peopleId = p_personId;
	RETURN count;
END$$
DELIMITER ;
