#!/bin/sh

N1=50000
N2=50000
N3=10000

SMALL_DIR="/home/lmy/Xlore/data/small/"
INSTANCE="xlore.instance.list.small.ttl"
CONCEPT="xlore.concept.list.small.ttl"
PROPERTY="xlore.property.list.small.ttl"
INFOBOX="xlore.instance.infobox.small.ttl"
TAXONOMY="xlore.taxonomy.small.ttl"
REFERENCE="xlore.instance.reference.small.ttl"
URL="xlore.instance.url.small.ttl"
MENTION="xlore.instance.mention.small.ttl"

ALL_DIR="/home/xlore/XloreData/etc/ttl/"
INSTANCE_ALL="xlore.instance.list.ttl"
CONCEPT_ALL="xlore.concept.list.ttl"
PROPERTY_ALL="xlore.property.list.ttl"
INFOBOX_ALL="xlore.instance.infobox.ttl"
TAXONOMY_ALL="xlore.taxonomy.ttl"
REFERENCE_ALL="xlore.instance.reference.ttl"
URL_ALL="xlore.instance.url.ttl"
MENTION_ALL="xlore.instance.mention.ttl"

# instance list
> $SMALL_DIR$INSTANCE
for i in $(seq $N1); do
    grep "^<$i>" $ALL_DIR$INSTANCE_ALL >> $SMALL_DIR$INSTANCE
done;

# concept list
> $SMALL_DIR$CONCEPT
for i in $(seq $N2); do
    grep "^<$i>" $ALL_DIR$CONCEPT_ALL >> $SMALL_DIR$CONCEPT
done;

# property list
> $SMALL_DIR$PROPERTY
for i in $(seq $N3); do
    grep "^<$i>" $ALL_DIR$PROPERTY_ALL >> $SMALL_DIR$PROPERTY
done;

# taxonomy
> $SMALL_DIR$TAXONOMY
for i in $(seq $N2); do
    grep "\/$i>" $ALL_DIR$TAXONOMY_ALL >> $SMALL_DIR$TAXONOMY
done;

# infobox
> $SMALL_DIR$INFOBOX
for i in $(seq $N3); do
    for j in $(seq $N1); do
        grep "\/property/$i>" $ALL_DIR$INFOBOX_ALL | grep "\/instance/$j>" >> $SMALL_DIR$INFOBOX
    done;
done;

# instance reference
> $SMALL_DIR$REFERENCE
for i in $(seq $N1); do
    grep "^<$i>" $ALL_DIR$REFERENCE_ALL >> $SMALL_DIR$REFERENCE
done;

# instance url
> $SMALL_DIR$URL
for i in $(seq $N); do
    grep "^<$i>" $ALL_DIR$URL_ALL >> $SMALL_DIR$URL
done;

# instance mention
> $SMALL_DIR$MENTION
for i in $(seq $N); do
    grep "^<$i>" $ALL_DIR$MENTION_ALL >> $SMALL_DIR$MENTION
done;

