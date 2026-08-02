-- Create views to allow users to only view their associated configurations --
CREATE VIEW `My_Configurations` AS
SELECT *
FROM `Components`
WHERE `Components`.`user_id` = @current_user_id -- This needs to be set once user logs in --