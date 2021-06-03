// Load Audiobooks
LOAD CSV WITH HEADERS FROM 'file:///audiobooks.csv' AS row_1
CREATE (ab:Audiobooks {bookId: row_1.books_id
	, category_name: row_1.category_name_1message
    , actual_size: row_1.actual_size
    , grade_level: row_1.grade_level
    , language: row_1.language
    })

// Load Users
LOAD CSV WITH HEADERS FROM 'file:///users.csv' AS row_2
CREATE (u:Users {userId: row_2.id
	, created_at: row_2.created_at
    , last_sign_in_at: row_2.last_sign_in_at
    , gender: row_2.gender
    , has_seen_onboarding: row_2.has_seen_onboarding
    , has_been_subscribed: row_2.has_been_subscribed
    })

// Load Audiobook_plays
LOAD CSV WITH HEADERS FROM 'file:///audiobook_plays.csv' AS row_3
CREATE (p:Audiobook_plays {playId: row_3.id
	, created_at: row_3.created_at
    , userId: row_3.user_id
    , BookId: row_3.audiobook_id
    , time_played: row_3.seconds
    })

// Create Relations
MATCH 


RETURN *