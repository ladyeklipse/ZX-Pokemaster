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
                if len(bundles)>1:
                    self.assignBundlesToFilesInBundles(bundles, depth_level)

    def enumerateFolders(self, collected_files, depth_level):
        folders = {}
        for game_name, files in collected_files.items():
            for i, file in enumerate(files):
                if not file:
                    continue
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
            'issues':value
        } for key, value in mini_bundles.items()]
        mini_bundles = self.organizeMiniBundlesByIssues(mini_bundles, depth_level)
        mini_bundles = sorted(mini_bundles, key=lambda x: x['name'])
        return mini_bundles

    def organizeMiniBundlesByIssues(self, mini_bundles, depth_level):
        for mini_bundle in mini_bundles:
            mini_bundle_folders = {}
            for file in mini_bundle['issues']:
                root_dir, bundled_part = file.getSplitDest(depth_level)
                folder = bundled_part.split('\\')[0]
                if folder not in mini_bundle_folders.keys():
                    mini_bundle_folders[folder] = []
                mini_bundle_folders[folder].append(file)
            mini_bundle['issues'] = mini_bundle_folders.copy()
        return mini_bundles

    def getBigBundlesFromMiniBundles(self, mini_bundles, depth_level):
        bundles = {}
        current_bundle = []
        while True:
            if mini_bundles:
                current_bundle.append(mini_bundles.pop(0)['issues'])
            issues_in_current_bundle = sum([len(mini_bundle) for mini_bundle in current_bundle])
            if mini_bundles:
                estimated_current_bundle_size = \
                    len(mini_bundles[0]['issues'])+issues_in_current_bundle
            else:
                estimated_current_bundle_size = 0
            if not mini_bundles or estimated_current_bundle_size >= self.max_files_per_folder:
                if current_bundle:
                    current_bundle_name = self.getBundleName(current_bundle, depth_level)
                    # bundles[current_bundle_name] = self.getFilesFromBundle(current_bundle)
                    bundles[current_bundle_name] = [issue for issue in current_bundle]
                current_bundle = []
            if not mini_bundles:
                break
        return bundles

    def getBundleName(self, bundle, depth_level):
        first_file = bundle[0][sorted(bundle[0].keys())[0]][0]
        last_file = bundle[-1][sorted(bundle[-1].keys())[-1]][-1]
        return '{}-{}'.format(first_file.getBundleName(depth_level),
                              last_file.getBundleName(depth_level))

    # def getFilesFromBundle(self, bundle):
    #     files = []
    #     for item in bundle:
    #         files += item.values()
    #     return files

    def splitLargeBundles(self, bundles):
        for bundle_name in list(bundles.keys()):
            bundle = bundles[bundle_name]
            if sum([len(x) for x in bundle])>self.max_files_per_folder:
                new_mini_bundles = self.splitBundle(bundle)
                for i, new_mini_bundle in enumerate(new_mini_bundles):
                    new_bundle_name=bundle_name+str(i+1) if i else bundle_name
                    bundles[new_bundle_name] = [new_mini_bundle]
        return bundles

    def splitBundle(self, bundle):
        def chunks(l, n):
            """Yield successive n-sized chunks from l."""
            for i in range(0, len(l), n):
                yield l[i:i + n]
        issues = list(itertools.chain(*bundle))
        new_mini_bundles = list(chunks(issues, self.max_files_per_folder))
        result = []
        for keys_list in new_mini_bundles:
            mini_bundle = {}
            for item in bundle:
                for key in item.keys():
                    if key in keys_list:
                        mini_bundle[key] = item[key]
            result.append(mini_bundle)
        return result
        # for chunk in chunks(issues, self.max_files_per_folder):
        #     new_mini_bundles.append([bundle[x] for x in chunk])
        return new_mini_bundles

    def assignBundlesToFilesInBundles(self, bundles, depth_level):
        for bundle_name, mini_bundles in bundles.items():
            for mini_bundle in mini_bundles:
                for issue in mini_bundle.values():
                    for file in issue:
                        file.setBundle(bundle_name, depth_level)
