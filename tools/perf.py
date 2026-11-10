#!/usr/bin/env python3
"""Performance log and analysis for a channel. Numbers go in a CSV that is only ever appended to,
so every day's snapshot is kept and growth over time can be measured.

  python3 tools/perf.py add <channel_dir> --ep ep001 --platform youtube --views 1200 --likes 40 --comments 6 \
        [--shares 3] [--avg-view-pct 71] [--followers-gained 5] [--date 2026-01-31] [--note "..."]
  python3 tools/perf.py followers <channel_dir> --platform youtube --total 132 [--date ...]
  python3 tools/perf.py report <channel_dir> [--min-hours 48]

`report` prints markdown: ranking, engagement rates, averages per episode attribute (every extra column in
episodes.csv such as category, hook_type, experiment), follower growth, and which episodes are still too
young to judge. It reports what the numbers say; explaining WHY is the analyst's job (see the analytics skill).
"""
import sys, os, csv, argparse, datetime, collections

PF = ['date', 'ep', 'platform', 'views', 'likes', 'comments', 'shares', 'avg_view_pct', 'followers_gained', 'note']
FF = ['date', 'platform', 'total']

def append(path, fields, row):
    new = not os.path.exists(path)
    with open(path, 'a', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        if new: w.writeheader()
        w.writerow({k: row.get(k, '') for k in fields})

def read(path):
    return list(csv.DictReader(open(path, encoding='utf-8'))) if os.path.exists(path) else []

def num(x):
    try: return float(str(x).replace(',', '').replace('%', ''))
    except ValueError: return 0.0

def report(chan, min_hours):
    rows = read(os.path.join(chan, 'performance.csv')); eps = {e['ep']: e for e in read(os.path.join(chan, 'episodes.csv'))}
    if not rows: print('No performance data yet. Log some with `perf.py add`.'); return
    latest = {}
    for r in rows:  # last snapshot per episode+platform wins
        k = (r['ep'], r['platform'])
        if k not in latest or r['date'] >= latest[k]['date']: latest[k] = r
    tot = collections.defaultdict(lambda: collections.defaultdict(float)); plats = collections.defaultdict(dict)
    for (ep, pf), r in latest.items():
        for m in ['views', 'likes', 'comments', 'shares', 'followers_gained']: tot[ep][m] += num(r[m])
        if r.get('avg_view_pct'): tot[ep]['_avp'] += num(r['avg_view_pct']); tot[ep]['_avn'] += 1
        plats[ep][pf] = int(num(r['views']))
    now = datetime.datetime.now(); stats = []
    for ep, t in tot.items():
        meta = eps.get(ep, {}); age = None
        if meta.get('publish_date'):
            try: age = (now - datetime.datetime.fromisoformat(meta['publish_date'])).total_seconds() / 3600
            except ValueError: pass
        v = t['views']; eng = (t['likes'] + t['comments'] + t['shares']) / v * 100 if v else 0
        stats.append({'ep': ep, 'views': int(v), 'eng': eng, 'likes': int(t['likes']), 'comments': int(t['comments']), 'shares': int(t['shares']),
                      'fol': int(t['followers_gained']), 'avp': t['_avp'] / t['_avn'] if t['_avn'] else None, 'age': age,
                      'young': age is not None and age < min_hours, 'meta': meta, 'plats': plats[ep]})
    mature = [s for s in stats if not s['young']]
    print(f'# Performance report — {os.path.basename(os.path.abspath(chan))} — {now:%Y-%m-%d}\n')
    print(f'{len(stats)} episodes with data, {len(mature)} old enough to judge (≥{min_hours}h since publish_date).\n')
    print('| ep | topic | views | eng % | likes | comments | shares | followers | avg view % | per platform | note |\n|---|---|---|---|---|---|---|---|---|---|---|')
    for s in sorted(stats, key=lambda s: -s['views']):
        print(f"| {s['ep']} | {s['meta'].get('topic','')[:40]} | {s['views']} | {s['eng']:.1f} | {s['likes']} | {s['comments']} | {s['shares']} | {s['fol']} | "
              f"{'' if s['avp'] is None else round(s['avp'])} | {', '.join(f'{k} {v}' for k, v in s['plats'].items())} | {'TOO EARLY' if s['young'] else ''} |")
    if len(mature) >= 2:
        med = sorted(s['views'] for s in mature)[len(mature) // 2]
        print(f'\nMedian views (mature episodes): {med}')
        top = sorted(mature, key=lambda s: -s['views'])[:3]; bot = sorted(mature, key=lambda s: s['views'])[:3]
        print('Top by views: ' + ', '.join(f"{s['ep']} ({s['views']})" for s in top))
        print('Bottom by views: ' + ', '.join(f"{s['ep']} ({s['views']})" for s in bot))
        print('Top by engagement rate: ' + ', '.join(f"{s['ep']} ({s['eng']:.1f}%)" for s in sorted(mature, key=lambda s: -s['eng'])[:3]))
        print('Top by followers gained: ' + ', '.join(f"{s['ep']} ({s['fol']})" for s in sorted(mature, key=lambda s: -s['fol'])[:3]))
        skip = {'ep', 'publish_date', 'topic', 'title', 'hook_text', 'notes', 'duration_s'}
        cols = [c for c in (next(iter(eps.values())).keys() if eps else []) if c not in skip]
        for c in cols:
            g = collections.defaultdict(list)
            for s in mature:
                if s['meta'].get(c): g[s['meta'][c]].append(s)
            if len(g) < 2: continue
            print(f'\n## By {c} (mature episodes; small groups are weak evidence)\n| {c} | episodes | avg views | avg eng % | avg followers |\n|---|---|---|---|---|')
            for k, ss in sorted(g.items(), key=lambda kv: -sum(x['views'] for x in kv[1]) / len(kv[1])):
                print(f"| {k} | {len(ss)} | {sum(x['views'] for x in ss)//len(ss)} | {sum(x['eng'] for x in ss)/len(ss):.1f} | {sum(x['fol'] for x in ss)/len(ss):.1f} |")
    else:
        print('\nNot enough mature episodes for comparisons yet — keep logging daily.')
    fol = read(os.path.join(chan, 'followers.csv'))
    if fol:
        print('\n## Followers\n| platform | first | latest | change | days |\n|---|---|---|---|---|')
        by = collections.defaultdict(list)
        for r in fol: by[r['platform']].append(r)
        for pf, rs in by.items():
            rs.sort(key=lambda r: r['date']); a, b = rs[0], rs[-1]
            days = (datetime.date.fromisoformat(b['date'][:10]) - datetime.date.fromisoformat(a['date'][:10])).days
            print(f"| {pf} | {int(num(a['total']))} ({a['date'][:10]}) | {int(num(b['total']))} ({b['date'][:10]}) | {int(num(b['total'])-num(a['total'])):+d} | {days} |")

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('add'); a.add_argument('channel'); a.add_argument('--ep', required=True); a.add_argument('--platform', required=True)
    for m in ['views', 'likes', 'comments', 'shares', 'avg-view-pct', 'followers-gained']: a.add_argument('--' + m, default='')
    a.add_argument('--date'); a.add_argument('--note', default='')
    f = sub.add_parser('followers'); f.add_argument('channel'); f.add_argument('--platform', required=True); f.add_argument('--total', required=True); f.add_argument('--date')
    r = sub.add_parser('report'); r.add_argument('channel'); r.add_argument('--min-hours', type=float, default=48)
    x = ap.parse_args(); today = datetime.date.today().isoformat()
    if x.cmd == 'add':
        append(os.path.join(x.channel, 'performance.csv'), PF, {'date': x.date or today, 'ep': x.ep, 'platform': x.platform, 'views': x.views, 'likes': x.likes,
               'comments': x.comments, 'shares': x.shares, 'avg_view_pct': x.avg_view_pct, 'followers_gained': x.followers_gained, 'note': x.note}); print('logged', x.ep, x.platform)
    elif x.cmd == 'followers':
        append(os.path.join(x.channel, 'followers.csv'), FF, {'date': x.date or today, 'platform': x.platform, 'total': x.total}); print('logged followers', x.platform)
    else: report(x.channel, x.min_hours)

if __name__ == '__main__':
    main()
