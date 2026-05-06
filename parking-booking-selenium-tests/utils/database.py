import logging
from contextlib import contextmanager
from typing import Iterator, Optional

import pymysql

from utils.config import Config

logger = logging.getLogger(__name__)


class DatabaseClient:
    """Optional DB helper for UI/API system tests.

    The current backend uses Sequelize with MySQL-compatible configuration.
    Keep all DB access disabled by default and use it only for assertions or
    cleanup of automation-owned data.
    """

    def __init__(self, config: Config):
        self.config = config

    @property
    def enabled(self) -> bool:
        return self.config.db_enable

    @contextmanager
    def connection(self) -> Iterator[pymysql.connections.Connection]:
        if not self.enabled:
            raise RuntimeError("Database checks are disabled. Set DB_ENABLE=true to use DB helpers.")
        if self.config.db_dialect.lower() != "mysql":
            raise RuntimeError("Only mysql DB_DIALECT is implemented for DB helpers.")

        conn = pymysql.connect(
            host=self.config.db_host,
            port=self.config.db_port,
            user=self.config.db_user,
            password=self.config.db_password,
            database=self.config.db_name,
            autocommit=False,
            cursorclass=pymysql.cursors.DictCursor,
        )
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def find_latest_reservation_by_plate(self, plate: str) -> Optional[dict]:
        if not self.enabled:
            logger.info("DB_ENABLE=false, skipping DB reservation lookup for plate=%s", plate)
            return None
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, dateIn, dateOut, startBlock, blockCount, plate, vehicleType, status, spotId
                    FROM Reservations
                    WHERE plate = %s
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (plate,),
                )
                return cur.fetchone()

    def find_spot_by_position(self, position: int, vehicle_type: str, slot_type: str) -> Optional[dict]:
        if not self.enabled:
            logger.info(
                "DB_ENABLE=false, skipping DB spot lookup for position=%s vehicle=%s slot=%s",
                position,
                vehicle_type,
                slot_type,
            )
            return None
        normalized_slot_type = str(slot_type).strip().upper()
        normalized_vehicle_type = str(vehicle_type).strip().upper()
        expected_area = None
        if normalized_vehicle_type == "CAR":
            expected_area = "A"
        elif normalized_vehicle_type == "MOTORBIKE":
            expected_area = "B"

        with self.connection() as conn:
            with conn.cursor() as cur:
                if expected_area:
                    cur.execute(
                        """
                        SELECT id, area, position, vehicleType, slotType, status, isActive, deletedAt
                        FROM Spots
                        WHERE area = %s
                          AND position = %s
                          AND UPPER(vehicleType) = %s
                          AND UPPER(slotType) = %s
                        ORDER BY id DESC
                        LIMIT 1
                        """,
                        (expected_area, position, normalized_vehicle_type, normalized_slot_type),
                    )
                else:
                    cur.execute(
                        """
                        SELECT id, area, position, vehicleType, slotType, status, isActive, deletedAt
                        FROM Spots
                        WHERE position = %s
                          AND UPPER(vehicleType) = %s
                          AND UPPER(slotType) = %s
                        ORDER BY id DESC
                        LIMIT 1
                        """,
                        (position, normalized_vehicle_type, normalized_slot_type),
                    )
                return cur.fetchone()

    def find_spot_by_id(self, spot_id: int) -> Optional[dict]:
        if not self.enabled:
            logger.info("DB_ENABLE=false, skipping DB spot lookup for id=%s", spot_id)
            return None
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, area, position, vehicleType, slotType, status, isActive, deletedAt
                    FROM Spots
                    WHERE id = %s
                    LIMIT 1
                    """,
                    (spot_id,),
                )
                return cur.fetchone()

    def find_staff_by_username(self, username: str) -> Optional[dict]:
        if not self.enabled:
            logger.info("DB_ENABLE=false, skipping DB staff lookup for username=%s", username)
            return None
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT username, name, date, role, status, deletedAt
                    FROM staff
                    WHERE username = %s
                    LIMIT 1
                    """,
                    (username,),
                )
                return cur.fetchone()

    def rollback_staff_by_username(self, username: str) -> int:
        if not self.enabled:
            logger.info("DB_ENABLE=false, skipping staff rollback for username=%s", username)
            return 0
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM staff WHERE username = %s", (username,))
                deleted_count = cur.rowcount
                logger.info("Rolled back %s staff row(s) for username=%s", deleted_count, username)
                return deleted_count

    def find_active_parking_rate(self, vehicle_type: str, ticket_type: str) -> Optional[dict]:
        if not self.enabled:
            logger.info("DB_ENABLE=false, skipping parking rate lookup for vehicle=%s ticket=%s", vehicle_type, ticket_type)
            return None
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT vehicleType, unitPrice, ticketType, status
                    FROM parkingRate
                    WHERE vehicleType = %s
                      AND ticketType = %s
                      AND status = 'active'
                    ORDER BY id DESC
                    LIMIT 1
                    """,
                    (vehicle_type, ticket_type),
                )
                return cur.fetchone()

    def rollback_reservations_by_plate_prefix(self, prefix: str) -> int:
        if not self.enabled:
            logger.info("DB_ENABLE=false, skipping reservation rollback for prefix=%s", prefix)
            return 0
        like_prefix = f"{prefix}%"
        with self.connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id FROM Reservations WHERE plate LIKE %s", (like_prefix,))
                ids = [row["id"] for row in cur.fetchall()]
                if not ids:
                    return 0

                placeholders = ",".join(["%s"] * len(ids))
                cur.execute(f"DELETE FROM Payments WHERE reservationId IN ({placeholders})", ids)
                cur.execute(f"DELETE FROM ReservationBlocks WHERE reservationId IN ({placeholders})", ids)
                cur.execute(f"DELETE FROM Reservations WHERE id IN ({placeholders})", ids)
                logger.info("Rolled back %s automation reservations", len(ids))
                return len(ids)
