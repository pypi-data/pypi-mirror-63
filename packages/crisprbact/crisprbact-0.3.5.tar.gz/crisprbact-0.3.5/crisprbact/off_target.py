import re
import pandas as pd

from crisprbact.utils import rev_comp


def compute_off_target_df(guide, seed_size, records, feature_df):
    """ Returns a pandas DataFrame with data about the identified off-targets.
    The features column contains a list of biopython SeqFeature objects that overlap
    with the off-target"""
    offs_df = get_off_target_pos(guide, records, seed_size)
    if offs_df is not None:
        offs_df["features"] = [
            get_pos_features(off.pampos, feature_df) for i, off in offs_df.iterrows()
        ]
        return offs_df
    else:
        return None


def get_off_target_pos(guide, recs, seed_size):
    if recs is not None:
        for rec in recs:
            offs_plus = re.finditer(guide[-seed_size:] + "[ATGC]GG", str(rec.seq))
            offs = list(
                gen_extract_off_target_strand_plus(offs_plus, rec, guide, seed_size)
            )
            # - ori
            offs_minus = re.finditer(
                "CC[ATGC]" + rev_comp(guide[-seed_size:]), str(rec.seq)
            )
            offs += list(
                gen_extract_off_target_strand_minus(offs_minus, rec, guide, seed_size)
            )
            offs_dict = dict(
                zip(
                    [
                        "start",
                        "end",
                        "pampos",
                        "strand",
                        "recid",
                        "max_matching_len",
                        "max_matching_seq",
                        "pam_seq",
                    ],
                    zip(*offs),
                )
            )
            return pd.DataFrame(offs_dict)
    else:
        return None


def get_pos_features(position, f_df):
    if len(f_df) > 0:
        feature_at_pos = f_df[(f_df.start < position) & (f_df.end > position)]
        return feature_at_pos.feature.values
    else:
        return []


def gen_extract_off_target_strand_plus(off_target_matches, rec, guide, seed_size):
    for match in off_target_matches:

        guide_subseq = guide[: 20 - seed_size][::-1]
        # extract part of the sequence
        seq_extension_len = len(guide) - seed_size
        start_pos_seq = match.start() - seq_extension_len
        end_pos_seq = match.end() - seed_size - 3
        sub_sequence_to_match = rec.seq[start_pos_seq:end_pos_seq][::-1]
        assert len(sub_sequence_to_match) == len(guide_subseq)
        matching_chars = list(common_start(sub_sequence_to_match, guide_subseq))
        matching_substr = "".join(matching_chars)
        yield match.span() + (
            match.end(),
            "+",
            rec.id,
            seed_size + len(matching_chars),
            matching_substr[::-1] + match.group(0)[:-3],
            match.group(0)[-3:],
        )


def common_start(seq1, seq2):
    for a, b in zip(seq1, seq2):
        if a == b:
            yield a
        else:
            return


def gen_extract_off_target_strand_minus(off_target_matches, rec, guide, seed_size):
    for match in off_target_matches:
        # Extract the sequence.
        # since rev_comp, extend the sequence to the end
        seq_extension_len = len(guide) - seed_size
        end_pos_seq = match.end() + seq_extension_len
        start_pos_seq = match.start() + seed_size + 3
        sub_sequence_to_match = rec.seq[start_pos_seq:end_pos_seq]

        # Extract part of the guide to match
        guide_subseq = rev_comp(guide[: 20 - seed_size])
        assert len(sub_sequence_to_match) == len(guide_subseq)

        matching_chars = list(common_start(sub_sequence_to_match, guide_subseq))
        matching_substr = "".join(matching_chars)
        yield match.span() + (
            match.start(),
            "-",
            rec.id,
            seed_size + len(matching_chars),
            match.group(0)[3:] + matching_substr,
            match.group(0)[:3],
        )


def extract_records(genome):
    records = list(genome)
    if records and len(records) > 0:
        return records
    else:
        return None


def extract_features(recs):

    if recs is not None:
        f_list = []
        for rec in recs:
            for f in rec.features:
                if f.type in ["CDS", "ncRNA", "rRNA", "tRNA"]:
                    f_list.append(
                        (
                            f.location.start.position,
                            f.location.end.position,
                            f.location.strand,
                            f.type,
                            f,
                            rec.id,
                        )
                    )
        f_dict = dict(
            zip(
                ["start", "end", "strand", "type", "feature", "recid"],
                zip(*f_list[1:]),
            )
        )  # starts at 1 to get rid of the first feature which is the whole chromosome
        return pd.DataFrame(f_dict)
    else:
        return None
