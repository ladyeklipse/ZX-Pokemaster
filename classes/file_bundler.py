import os
import itertools

class FileBundler():

    def __init__(self, max_files_per_folder, depth):
        self.max_files_per_folder = max_files_per_folder
        self.depth = depth

    def bundleFilesInEqualFolders(self, collected_files):
        for depth_level in range(self.depth):
            folders = self.enumerateFolders(collected_files, depth_level)
            for folder_name, files in folders.items():
                if len(files)<=self.max_files_per_folder:
                    continue
                mini_bundles = self.getMiniBundlesFromFilesList(files, depth_level)
                bundles = self.getBigBundlesFromMiniBundles(mini_bundles, depth_level)
                bundles = self.splitLargeBundles(bundles)
                self.assignBundlesToFilesInBundles(bundles, depth_level)

    def enumerateFolders(self, collected_files, depth_level):
        folders = {}
        for game_wos_id, files in collected_files.items():
            for i, file in enumerate(files):
                if not file:
                    continue
                # file_dest_dir = os.path.dirname(file.getDestPath())
                file_dest_dir, bundled_part = file.getSplitDest(depth_level=depth_level)
                if not folders.get(file_dest_dir):
                    folders[file_dest_dir]=[]
                folders[file_dest_dir].append(file)
        return folders

    def getMiniBundlesFromFilesList(self, files, depth_level):
        mini_bundles = {}
        for file in files:
            mini_bundle_name = file.getBundleName(depth_level)
            if not mini_bundles.get(mini_bundle_name):
                mini_bundles[mini_bundle_name] = []
            mini_bundles[mini_bundle_name].append(file)
        mini_bundles = [{
            'name':key,
            'files':value
        } for key, value in mini_bundles.items()]
        mini_bundles = sorted(mini_bundles, key=lambda x: x['name'])
        return mini_bundles

    def getBigBundlesFromMiniBundles(self, mini_bundles, depth_level):
        bundles = {}
        current_bundle = []
        while True:
            if mini_bundles:
                current_bundle.append(mini_bundles.pop(0)['files'])
            files_in_current_bundle = sum([len(bundle) for bundle in current_bundle])
            if mini_bundles:
                estimated_current_bundle_size = \
                    len(mini_bundles[0]['files'])+files_in_current_bundle
            else:
                estimated_current_bundle_size = 0
            if not mini_bundles or estimated_current_bundle_size >= self.max_files_per_folder:
                if current_bundle:
                    current_bundle_name = self.getBundleName(current_bundle, depth_level)
                    # if estimated_current_bundle_size>self.max_files_per_folder:
                    #     new_bundles = self.splitBundle(current_bundle)
                    #     for i, bundle in enumerate(new_bundles):
                    #         bundle_name = current_bundle_name
                    #         if i>1:
                    #             bundle_name+=str(i)
                    #         bundles[bundle_name] = bundle
                    # else:
                    bundles[current_bundle_name] = [file for file in current_bundle]
                current_bundle = []
            if not mini_bundles:
                break
        return bundles

    def getBundleName(self, bundle, depth_level):
        return '{}-{}'.format(bundle[0][0].getBundleName(depth_level),
                              bundle[-1][-1].getBundleName(depth_level))

    def splitLargeBundles(self, bundles):
        for bundle_name in list(bundles.keys()):
            bundle = bundles[bundle_name]
            if sum([len(x) for x in bundle])>self.max_files_per_folder:
                new_mini_bundles = self.splitBundle(bundle)
                for i, new_mini_bundle in enumerate(new_mini_bundles):
                    new_bundle_name=bundle_name+str(i+1) if i else bundle_name
                    bundles[new_bundle_name] = [new_mini_bundle]
            # del bundles[bundle_name]
        return bundles

    def splitBundle(self, bundle):
        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]
        files = list(itertools.chain(*bundle))
        new_mini_bundles = list(chunks(files, self.max_files_per_folder))
        # new_bundles = list(chunks(bundle, self.max_files_per_folder))
        return new_mini_bundles

    def assignBundlesToFilesInBundles(self, bundles, depth_level):
        for bundle_name, mini_bundles in bundles.items():
            for mini_bundle in mini_bundles:
                for file in mini_bundle:
                    file.setBundle(bundle_name, depth_level)
