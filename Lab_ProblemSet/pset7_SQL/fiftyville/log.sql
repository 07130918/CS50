-- Keep a log of any SQL queries you execute as you solve the mystery.
-- URL https://cs50.jp/x/2021/week7/problem-set/fiftyville/

-- 犯罪の日付と場所に一致する犯罪現場レポートを探す
SELECT * FROM crime_scene_reports
WHERE year = 2020 AND month = 7 AND day = 28 AND street = 'Chamberlin Street';

-- 犯罪現場レポート(discription)から2020年7月28日にインタビューが行われたことがわかった
SELECT * FROM interviews
WHERE year = 2020 AND month = 7 AND day = 28;
-- 上記で検索すると6件取れてそのうち匂う証言が3つあった
SELECT * FROM interviews
WHERE id = 161 OR id = 162 OR id = 163;

-- 絞り込み1
-- Ruth(8レコード), Eugene(9レコード)両方の証言で呼び出される候補が4人
SELECT * FROM people
-- ナンバープレートから個人を特定する(このWHERE句で8レコード取れる)
WHERE license_plate  IN (
    -- Ruthの発言から2020/7/28 10:15~10:25のセキュリティ映像を確認しナンバープレートを取得
    SELECT license_plate FROM courthouse_security_logs
    WHERE year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25
    AND activity = 'exit'
) AND id IN (
    -- 特定したaccount_numberからperson_idを特定(people.idが最終的に欲しいため)
    SELECT person_id FROM bank_accounts
    WHERE account_number IN (
        -- Eugeneの発言から2020/7/28にFifer StreetのATMを利用したaccount_numberを特定
        SELECT account_number FROM atm_transactions
        WHERE year = 2020 AND month = 7 AND day = 28 AND atm_location = 'Fifer Street'
    )
)
ORDER BY name;

-- 29日Fiftyvilleから出る1番早いフライトのidと着陸する空港のidを取得
SELECT id, destination_airport_id FROM flights
WHERE day = 29 AND origin_airport_id = (
    SELECT id FROM airports
    WHERE city = 'Fiftyville'
)
ORDER BY hour LIMIT 1;

-- 着陸する空港のid(destination_airport_id)をもとに逃亡先(city)を特定
SELECT city FROM airports
WHERE id = 4;

-- 絞り込み2
-- Raymondの証言(5レコード)
SELECT * FROM people
WHERE passport_number IN (
    -- 犯人はflight_id = 36に搭乗する(8レコード)
    SELECT passport_number FROM passengers
    WHERE flight_id = 36
) AND phone_number IN (
    -- 2020/7/28に1分未満の電話をかけている人(9レコード)
    SELECT caller FROM phone_calls
    WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60
);

-- 絞り込み1と2(3人の証言)で1レコード重なるためその人が犯人"Ernest"

-- 共犯探し
-- Ernestが事件の日誰に電話を掛けたを特定
SELECT name, phone_number FROM people
WHERE phone_number = (
    SELECT receiver FROM phone_calls
    WHERE caller IN (
        SELECT phone_number FROM people
        WHERE name = 'Ernest'
    ) AND year = 2020 AND month = 7 AND day = 28 AND duration < 60
);
