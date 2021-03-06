CREATE TABLE Users (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `name` varchar(32) NOT NULL DEFAULT '',
    `rating` tinyint signed NOT NULL DEFAULT -1,
    `salt` varchar(40) NOT NULL,
    `passwd_hash` varchar(40) NOT NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `name_idx` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Sessions (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `user_id` int(11) unsigned NOT NULL,
    `data` text,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `user_id_idx` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Games (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `status` tinyint unsigned NOT NULL,
    `current_seq` smallint unsigned NOT NULL default 1,
    PRIMARY KEY (`id`),
    INDEX `status_idx` (`status`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Players (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `game_id` int(11) unsigned NOT NULL,
    `user_id` int(11) unsigned NOT NULL,
    `color` tinyint unsigned NOT NULL,
    PRIMARY KEY (`id`),
    INDEX `game_id_user_id_idx` (`game_id`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Votes (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `game_id` int(11) unsigned NOT NULL,
    `user_id` int(11) unsigned NOT NULL,
    `seq` smallint unsigned NOT NULL,
    `move` varchar(5) NOT NULL,
    `notes` varchar(1024) NOT NULL DEFAULT '',
    `ip_address` varchar(16) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`),
    UNIQUE INDEX `game_id_seq_user_id_idx` (`game_id`, `seq`, `user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Comments (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `game_id` int(11) unsigned NOT NULL,
    `user_id` int(11) unsigned NOT NULL,
    `seq` smallint unsigned NOT NULL,
    `move` varchar(5) NOT NULL,
    `notes` varchar(1024) NOT NULL DEFAULT '',
    `ip_address` varchar(16) NOT NULL DEFAULT '',
    PRIMARY KEY (`id`),
    UNIQUE INDEX `game_id_seq_user_id_move_idx` (`game_id`, `seq`, `user_id`, `move`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Game_States (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `game_id` int(11) unsigned NOT NULL,
    `seq` smallint unsigned NOT NULL default 0,
    `black_captures` smallint unsigned NOT NULL default 0,
    `white_captures` smallint unsigned NOT NULL default 0,
    `illegal` text not NULL,
    `board` text not NULL,
    `sgf` text not NULL,
    PRIMARY KEY (`id`),
    UNIQUE INDEX `game_id_seq_idx` (`game_id`, `seq`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE System_Message (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `message` text,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE Chat_Messages (
    `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
    `created` timestamp NOT NULL default current_timestamp,
    `room_id` int(11) unsigned NOT NULL,
    `user_id` int(11) unsigned NOT NULL,
    `message` varchar(1024) NOT NULL DEFAULT '',
    `deleted` tinyint(1) NOT NULL default 0,
    PRIMARY KEY (`id`),
    INDEX `room_id_id` (`room_id`, `id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
