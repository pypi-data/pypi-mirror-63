import os
from copy import deepcopy

from mlbench_core.dataset.translation.pytorch import config
from torchtext.data import Example, Dataset


def _construct_filter_pred(min_len, max_len):
    filter_pred = lambda x: not (len(x[0]) < min_len or len(x[1]) < min_len)
    if max_len is not None:
        filter_pred = lambda x: not (
            len(x[0]) < min_len
            or len(x[0]) > max_len
            or len(x[1]) < min_len
            or len(x[1]) > max_len
        )

    return filter_pred


def process_data(path, filter_pred, fields, lazy=False):
    """
    Loads data from the input file.
    """

    src_path, trg_path = tuple(os.path.expanduser(path + x) for x in config.EXTS)
    examples = []
    with open(src_path, mode="r", encoding="utf-8") as src_file, open(
        trg_path, mode="r", encoding="utf-8"
    ) as trg_file:
        for src_line, trg_line in zip(src_file, trg_file):
            src_line, trg_line = src_line.strip(), trg_line.strip()

            should_consider = filter_pred((src_line, trg_line))
            if src_line != "" and trg_line != "" and should_consider:
                if lazy:
                    examples.append((src_line, trg_line))
                else:
                    examples.append(Example.fromlist([src_line, trg_line], fields))
    return examples


class WMT14Dataset(Dataset):
    urls = [
        (
            "https://drive.google.com/uc?export=download&"
            "id=0B_bZck-ksdkpM25jRUN2X2UxMm8",
            "wmt16_en_de.tar.gz",
        )
    ]
    name = "wmt14"
    dirname = ""

    def __init__(
        self,
        root,
        tokenizer,
        download=True,
        train=False,
        validation=False,
        lazy=False,
        min_len=0,
        max_len=None,
    ):
        """WMT14 Dataset.

        Loads WMT14 dataset.
        Based on `torchtext.datasets.WMT14`

        Args:
            root (str): Root folder of WMT14 dataset
            download (bool): Download dataset
            train (bool): Whether to get the train or validation set.
                Default=True
            batch_first (bool): if True the model uses (batch,seq,feature)
                tensors, if false the model uses (seq, batch, feature)
        """

        self.lazy = lazy

        src_tokenizer = deepcopy(tokenizer)
        src_tokenizer.set_is_target(False)
        trg_tokenizer = deepcopy(tokenizer)
        trg_tokenizer.set_is_target(True)

        self.list_fields = [("src", src_tokenizer), ("trg", trg_tokenizer)]
        super(WMT14Dataset, self).__init__(examples=[], fields={})

        self.fields = dict(self.list_fields)
        self.max_len = max_len
        self.min_len = min_len
        if download:
            path = self.download(root)
        else:
            path = os.path.join(root, "wmt14")

        if train:
            path = os.path.join(path, config.TRAIN_FNAME)
        elif validation:
            path = os.path.join(path, config.VAL_FNAME)
        else:
            raise NotImplementedError()

        self.examples = process_data(
            path,
            filter_pred=_construct_filter_pred(min_len, max_len),
            fields=self.list_fields,
            lazy=lazy,
        )

    @property
    def vocab_size(self):
        return self.fields["src"].vocab_size

    def get_special_token_idx(self, token):
        return self.fields["src"].get_special_token_indices()[token]

    def get_raw_item(self, idx):
        return super().__getitem__(idx)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, item):
        if self.lazy:
            src_line, trg_line = self.examples[item]
            return Example.fromlist([src_line, trg_line], self.list_fields)
        else:
            return self.examples[item]

    def __iter__(self):
        for x in self.examples:
            if self.lazy:
                src_line, trg_line = x
                yield Example.fromlist([src_line, trg_line], self.list_fields)
            else:
                yield x
