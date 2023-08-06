local limits = cjson.decode(ARGV[1])
local now = ARGV[2]
local api_id = ARGV[3]
local existing_tickets
local wait_time = 0
local gap = 0
local recycled_key = ''

-- search for free slot and collect wait_time if there is none
for i, limit in ipairs(limits) do
    local duration = limit[1]
    local ticket = 'RL:' .. api_id .. ':' .. i .. ':*'
    local min_ttl = 0

    local existing_tickets = redis.call('keys', ticket)
    redis.log(redis.LOG_WARNING, 'Searching for ticket pattern: ' .. ticket ..
            ', found: ' .. table.getn(existing_tickets))

    local tmp_key = ''

    if table.getn(existing_tickets) >= limit[2] then
        for _,key in ipairs(existing_tickets) do
            local ttl = redis.call('pttl', key)
            local value = redis.call('get', key)
            if value ~= 'recycled' then
                if min_ttl == 0 then
                    min_ttl = ttl
                    tmp_key = key
                elseif ttl < min_ttl then
                    min_ttl = ttl
                    tmp_key = key
                end
            end
        end
    end

    -- if tmp_key is '' and we are over the limit  then all tickets
    -- in the current bucket are already recycled (!) -> what to do ?

    if table.getn(existing_tickets) < limit[2] then
        -- there's a free slot in this bucket
        local tmp = limit[1] / limit[2]
        if gap == 0 then
            gap = tmp
        elseif tmp < gap then
            gap = tmp
        end

        gap = gap * 1000
        redis.log(redis.LOG_WARNING, 'Using FREE SLOT, gap time: ' .. gap)
    end

    if wait_time < min_ttl then
        wait_time = min_ttl
        recycled_key = tmp_key
    end

end

-- mark the key as expired if we are going to recycle a ticket
-- after a wait period
if recycled_key ~= '' then
    redis.call('mset', recycled_key, 'recycled')
    local check_ttl = redis.call('pttl', recycled_key)
    if check_ttl == -1 then
        redis.call('del', recycled_key)
    end
end
redis.log(redis.LOG_WARNING, 'Recycled key: ' .. recycled_key)
redis.log(redis.LOG_WARNING, 'Resulting wait_time: ' .. wait_time ..
        'ms + gap ' .. gap .. 'ms')
redis.log(redis.LOG_WARNING, 'Creating new tickets:')
-- create new ticket, one for each type and set expiration
for i, limit in ipairs(limits) do
    -- add wait_time to the expiration
    local exp = (limit[1] * 1000) + wait_time
    local exp_ns = (exp * 1000000) + now
    -- local exp_ns_str = string.format("%.0f", exp_ns)
    redis.log(redis.LOG_WARNING, 'Ticket: RL:' .. api_id .. ':' .. i ..
            ':' .. now .. ', expiration: ' .. exp .. 'ms')
    redis.call('mset', 'RL:' .. api_id .. ':'.. i .. ':' .. now, 'exp_ns_str')
    local result = redis.call('pexpire', 'RL:' .. api_id .. ':' .. i .. ':' ..
            now, exp)
    local ttlko = redis.call('pttl', 'RL:' .. api_id .. ':' .. i .. ':' .. now)
end

-- notice: resulting wait time is in miliseconds
-- calling side is obligued to wait for that amount of time on its own
-- _immediately_
return wait_time + gap
