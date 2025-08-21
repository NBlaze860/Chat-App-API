-- =============================================================================
-- database_schema.sql - Complete database setup for chat app
-- =============================================================================

-- Drop existing tables if they exist (only for fresh setup)
-- DROP TABLE IF EXISTS messages;
-- DROP TABLE IF EXISTS chats;

-- Create chats table to track conversations between users
CREATE TABLE chats (
    chat_id TEXT PRIMARY KEY,
    user1_id TEXT NOT NULL,
    user2_id TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_message_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create messages table to store all chat messages
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    chat_id TEXT NOT NULL REFERENCES chats(chat_id),
    sender_id TEXT NOT NULL,
    receiver_id TEXT NOT NULL,
    message_text TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for optimal query performance
CREATE INDEX idx_messages_chat_id_created ON messages (chat_id, created_at);
CREATE INDEX idx_chats_user1 ON chats (user1_id, last_message_at DESC);
CREATE INDEX idx_chats_user2 ON chats (user2_id, last_message_at DESC);
CREATE INDEX idx_chats_users ON chats (user1_id, user2_id);

-- Optional: Add RLS (Row Level Security) if needed
-- ALTER TABLE chats ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Optional: Create policies for RLS
-- CREATE POLICY "Users can access their own chats" ON chats
--     FOR ALL USING (auth.uid()::text = user1_id OR auth.uid()::text = user2_id);

-- CREATE POLICY "Users can access their own messages" ON messages
--     FOR ALL USING (auth.uid()::text = sender_id OR auth.uid()::text = receiver_id); 