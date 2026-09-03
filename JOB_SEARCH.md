# Daily Brand & Marketing Job Search

Automated morning sweep for senior brand & marketing roles, logged into Notion.

## Where things live

- **Notion Tracker (database):** https://app.notion.com/p/bbfd547a7c8c43f29019a8ee1a691695
- **Notion Control Center (routine + Search Hub links):** https://app.notion.com/p/37943b27b9cc8104892de2567e16edec

## Criteria

| Dimension | Rule |
|---|---|
| **Functions** | Head of Brand, Head of Marketing, Creative Director, Brand Strategist, Brand Manager, VP Marketing, Partnerships, Strategy (+ Brand Director, CMO) |
| **Industries** | Blockchain/Web3, Tech, Sport Tech, Fashion, Lifestyle/Wellness, Gen AI |
| **Stage** | Series A or B preferred; Series C sometimes. For Gen AI: solid market presence, long runway, profitable. |
| **Salary** | $120k+ /yr (or local equivalent) |
| **Location** | Remote or Hybrid anywhere; on-site only in Europe, NYC, LA, SF, Dubai |
| **Freshness** | Posted within the last 2 months, and confirmed still live |

## The triple-check (every role must pass all 3)

1. **Still live** — original posting loads, not marked closed, still on the company careers page.
2. **Fresh (< 2 months)** — posted within 8 weeks; if only "30+ days ago" shows, confirm on the company site.
3. **On-criteria** — stage, comp ($120k+), and location/work-mode all match. Note gaps in the row.

## How the "every morning" automation works

This cloud environment is ephemeral, so the recurrence is driven by a **scheduled trigger**
(a Routine that spawns a fresh session each morning), not a long-running process. The Routine
is already created; it runs daily and each firing appends new vetted roles to the Notion tracker.
A daily **Google Calendar** reminder backs it up as a manual fallback.

### Daily prompt (what the scheduled Routine runs)

```
Run today's brand & marketing job sweep. Read JOB_SEARCH.md for criteria.
Work through the Search Hub links in the Notion Control Center
(https://app.notion.com/p/37943b27b9cc8104892de2567e16edec). Also check Gen AI companies
(Higgsfield, Magnific/Freepik, ElevenLabs, Runway, HeyGen, Synthesia, Luma, Photoroom,
Perplexity, Midjourney, and peers with solid market presence + long runway + profitable) for
Marketing / Partnerships / Strategy roles. For each new role that matches the criteria, add a
row to the Notion tracker (data source d6972fd4-fd44-4ba6-b0fc-f19439f44c96) with Role, Company,
Function, Industry, Stage, Location, Work Mode, Salary, Min Salary USD, Posted date, Source,
Link, Date Added = today, Status = "To verify". Apply the triple-check and note any gaps. Skip
duplicates already in the tracker. Mark stale/filled roles Closed/expired. Keep it well-organised.
```

## Manual fallback

If a scheduled trigger isn't available, open the **Control Center** each morning and
click through the Search Hub links yourself — they're pre-filtered to recent postings
and sorted newest-first.

## Note on verification limits

LinkedIn, most job boards, and even Greenhouse/Ashby careers boards block logged-out/automated
fetching from this environment (egress-blocked), so live status cannot be auto-verified here.
The Search Hub links are the fastest manual path; the triple-check is completed by clicking
through in a logged-in browser.
