DELIMITER $$
CREATE DEFINER=`root`@`%` PROCEDURE `rate`(
    IN p_movShowId VARCHAR(12), 
    IN p_rating DOUBLE
)
BEGIN
    DECLARE v_avgRating DOUBLE;
    DECLARE v_numVotes INT;

    -- Prevent NULL ratings
    IF p_rating IS NULL THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Rating value cannot be NULL.';
    END IF;

    IF EXISTS (SELECT 1 FROM Ratings WHERE movShowId = p_movShowId) THEN
        -- Ensure column names match the table's actual columns
        SELECT avgRating, numVotes
        INTO v_avgRating, v_numVotes
        FROM Ratings
        WHERE movShowId = p_movShowId;

        -- Calculate new average
        SET v_avgRating = (v_numVotes * v_avgRating + p_rating) / (v_numVotes + 1);
        SET v_numVotes = v_numVotes + 1;

        UPDATE Ratings
        SET avgRating = v_avgRating, numVotes = v_numVotes
        WHERE movShowId = p_movShowId;
    ELSE
        -- Insert new record with valid rating
        INSERT INTO Ratings (movShowId, avgRating, numVotes)
        VALUES (p_movShowId, p_rating, 1);
    END IF;
END$$
DELIMITER ;
