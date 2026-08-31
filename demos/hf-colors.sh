#!/bin/sh
# Free Hugging Face Space colour combinations for one or more owners.
#
#   sh hf-colors.sh <owner[,owner2,...]> [-emoji]
#
# or straight from the site, which is what an agent wants:
#
#   curl -s https://katehuuh.github.io/demos/hf-colors.sh | sh -s -- Luminia,WeReCooking -emoji
#
# Prints, as plain text:
#   AVAILABLE n/64   every colorFrom->colorTo pair nobody in the list uses yet
#   USED n           the pairs that are taken, count in brackets when repeated
#   EMOJI n          with -emoji, the emoji already taken, same bracket rule
#
# Reads the public Hugging Face API. No key, no account, no server. Works for
# users and orgs alike. One request per owner, capped at 1000 spaces each.
set -eu

if [ $# -lt 1 ]; then
  echo "usage: hf-colors.sh <owner[,owner2,...]> [-emoji]" >&2
  exit 2
fi

owners=$(echo "$1" | tr ',' ' ')
shift
want_emoji=false
[ "${1:-}" = "-emoji" ] && want_emoji=true

for o in $owners; do
  curl -sS "https://huggingface.co/api/spaces?author=$o&expand[]=cardData&limit=1000"
done | jq -s --argjson emoji "$want_emoji" -r '
  def C: ["red","yellow","green","blue","indigo","purple","pink","gray"];
  def tally: group_by(.) | map({k:.[0], n:length}) | sort_by(-.n, .k);
  def show: map(if .n > 1 then "\(.k) (\(.n))" else .k end);
  ([.[][] | .cardData // {}]) as $cards
  | ([$cards[] | select(.colorFrom and .colorTo) | "\(.colorFrom)->\(.colorTo)"]) as $used
  | ([C[] as $a | C[] as $b | "\($a)->\($b)"]) as $all
  | ($used | tally) as $cnt
  | ($all - ($used | unique)) as $free
  | ([$cards[] | .emoji // empty] | tally) as $emo
  | ( ["AVAILABLE \($free|length)/\($all|length)"] + $free
    + ["", "USED \($cnt|length)"] + ($cnt | show)
    + (if $emoji then ["", "EMOJI \($emo|length)"] + ($emo | show) else [] end)
    ) | .[]
'
