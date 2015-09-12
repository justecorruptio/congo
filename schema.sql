CREATE TABLE Users (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(32) NOT NULL DEFAULT '',
    `rating` tinyint signed NOT NULL DEFAULT -1,
    `salt` varchar(40) NOT NULL,
    `passwd_hash` varchar(40) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `name_idx` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Sessions (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `user_id` int(11) unsigned NOT NULL,
    `created` timestamp NOT NULL default current_timestamp,
    `data` text,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `user_id_idx` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
