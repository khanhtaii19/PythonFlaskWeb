import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host':     os.getenv('MYSQL_HOST', 'localhost'),
    'port':     int(os.getenv('MYSQL_PORT', 3306)),
    'user':     os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'db':       os.getenv('MYSQL_DB', 'gourmet_shop'),
    'charset':  'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
    'autocommit': True
}


def get_db():
    """Return a new DB connection."""
    return pymysql.connect(**DB_CONFIG)


def init_db():
    """Create all tables if they don't exist yet."""
    sql_statements = [
        # ─── users ───────────────────────────────────────────────
        """
        CREATE TABLE IF NOT EXISTS users (
            id          VARCHAR(36)  PRIMARY KEY DEFAULT (UUID()),
            name        VARCHAR(255) NOT NULL,
            email       VARCHAR(255) NOT NULL UNIQUE,
            password    VARCHAR(255) NOT NULL,
            phone       VARCHAR(20),
            role        ENUM('user','admin') DEFAULT 'user',
            member_level ENUM('Silver','Gold','Diamond') DEFAULT 'Silver',
            total_spent DECIMAL(15,2) DEFAULT 0,
            avatar      TEXT,
            is_active   TINYINT(1) DEFAULT 1,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # ─── categories ──────────────────────────────────────────
        """
        CREATE TABLE IF NOT EXISTS categories (
            id          VARCHAR(36)  PRIMARY KEY DEFAULT (UUID()),
            name        VARCHAR(255) NOT NULL UNIQUE,
            description TEXT         NOT NULL,
            image       TEXT         NOT NULL,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # ─── products ────────────────────────────────────────────
        """
        CREATE TABLE IF NOT EXISTS products (
            id             VARCHAR(36)  PRIMARY KEY DEFAULT (UUID()),
            category_id    VARCHAR(36),
            name           VARCHAR(255) NOT NULL,
            description    TEXT         NOT NULL,
            details        TEXT         NOT NULL,
            price          DECIMAL(15,2) NOT NULL,
            sale_price     DECIMAL(15,2),
            cost_price     DECIMAL(15,2) NOT NULL DEFAULT 0,
            stock          INT          NOT NULL DEFAULT 0,
            total_sold     INT          DEFAULT 0,
            image          TEXT         NOT NULL,
            promotion_text VARCHAR(500),
            created_at     DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at     DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # ─── orders ──────────────────────────────────────────────
        """
        CREATE TABLE IF NOT EXISTS orders (
            id              VARCHAR(36)  PRIMARY KEY DEFAULT (UUID()),
            user_id         VARCHAR(36)  NOT NULL,
            total_amount    DECIMAL(15,2) NOT NULL,
            discount_amount DECIMAL(15,2) DEFAULT 0,
            final_amount    DECIMAL(15,2) NOT NULL,
            coupon_code     VARCHAR(50),
            status          ENUM('pending','paid','processing','shipped','delivered','cancelled') DEFAULT 'pending',
            payment_method  ENUM('credit_card','cash','bank_transfer') NOT NULL,
            street          VARCHAR(500),
            city            VARCHAR(255),
            state           VARCHAR(255),
            zip_code        VARCHAR(20),
            country         VARCHAR(255),
            notes           TEXT,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # ─── order_items ─────────────────────────────────────────
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id          VARCHAR(36)   PRIMARY KEY DEFAULT (UUID()),
            order_id    VARCHAR(36)   NOT NULL,
            product_id  VARCHAR(36),
            quantity    INT           NOT NULL,
            price       DECIMAL(15,2) NOT NULL,
            FOREIGN KEY (order_id)   REFERENCES orders(id)   ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # ─── coupons ─────────────────────────────────────────────
        """
        CREATE TABLE IF NOT EXISTS coupons (
            id               VARCHAR(36) PRIMARY KEY DEFAULT (UUID()),
            code             VARCHAR(50) NOT NULL UNIQUE,
            discount_percent INT         NOT NULL,
            `limit`          INT         NOT NULL,
            used_count       INT         DEFAULT 0,
            expiry_date      DATE        NOT NULL,
            is_active        TINYINT(1)  DEFAULT 1,
            created_at       DATETIME    DEFAULT CURRENT_TIMESTAMP,
            updated_at       DATETIME    DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """,

        # ─── blog_posts ──────────────────────────────────────────
        """
        CREATE TABLE IF NOT EXISTS blog_posts (
            id           VARCHAR(36)  PRIMARY KEY DEFAULT (UUID()),
            title        VARCHAR(500) NOT NULL,
            excerpt      TEXT         NOT NULL,
            content      LONGTEXT     NOT NULL COMMENT 'JSON array of paragraphs',
            post_date    DATETIME     DEFAULT CURRENT_TIMESTAMP,
            category     VARCHAR(255) NOT NULL,
            image        TEXT         NOT NULL,
            author_name  VARCHAR(255) NOT NULL,
            author_avatar TEXT,
            author_read_time VARCHAR(50),
            tags         TEXT COMMENT 'JSON array of tags',
            created_at   DATETIME     DEFAULT CURRENT_TIMESTAMP,
            updated_at   DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    ]

    conn = get_db()
    try:
        with conn.cursor() as cursor:
            for stmt in sql_statements:
                cursor.execute(stmt)
        print("✅ Database tables initialised")
    except Exception as e:
        print(f"❌ DB init error: {e}")
        raise
    finally:
        conn.close()
