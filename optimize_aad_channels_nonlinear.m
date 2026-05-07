function result = optimize_aad_channels_nonlinear(scores, varargin)
%OPTIMIZE_AAD_CHANNELS_NONLINEAR Non-linear channel reduction helper for AAD pipelines.
%
% This is a MATLAB port of the Python helper in this repository.
%
% Selects the smallest subset of channels whose nonlinearly-weighted scores
% account for at least `retention_target` of the total, while always selecting
% at least `min_channels`.
%
% Non-linear emphasis uses score.^gamma so high-value channels contribute more.
%
% Parameters
% ----------
% scores : vector
%   Non-negative channel scores.
%
% Name-value pairs
% ----------------
% retention_target : scalar in (0,1], default 0.95
% gamma            : positive scalar, default 1.5
% min_channels     : positive integer, default 1
%
% Returns
% -------
% result : struct with fields
%   selected_indices : 1-based indices of selected channels (sorted)
%   retained_ratio   : retained weighted ratio (in [0,1])
%
% Notes
% -----
% - MATLAB uses 1-based indices (Python version uses 0-based).
% - If all weighted scores sum to 0, returns 1:min_channels and retained_ratio=1.

p = inputParser;
p.FunctionName = mfilename;
addRequired(p, 'scores', @(x) isnumeric(x) && isvector(x));
addParameter(p, 'retention_target', 0.95, @(x) isnumeric(x) && isscalar(x));
addParameter(p, 'gamma', 1.5, @(x) isnumeric(x) && isscalar(x));
addParameter(p, 'min_channels', 1, @(x) isnumeric(x) && isscalar(x) && isfinite(x));
parse(p, scores, varargin{:});

values = double(p.Results.scores(:)');
retention_target = double(p.Results.retention_target);
gamma = double(p.Results.gamma);
min_channels = double(p.Results.min_channels);

if isempty(values)
    error('scores must not be empty');
end
if ~(retention_target > 0 && retention_target <= 1)
    error('retention_target must be in the range (0, 1]');
end
if ~(gamma > 0)
    error('gamma must be positive');
end
if ~(min_channels >= 1 && mod(min_channels,1)==0)
    error('min_channels must be at least 1');
end
if min_channels > numel(values)
    error('min_channels cannot exceed number of input scores');
end
if any(values < 0)
    error('scores must be non-negative');
end

weighted = values .^ gamma;
total = sum(weighted);

if total == 0
    result.selected_indices = 1:min_channels;
    result.retained_ratio = 1.0;
    return;
end

[sorted_weight, order] = sort(weighted, 'descend'); %#ok<ASGLU>
selected = zeros(1,0);
running = 0.0;

for k = 1:numel(order)
    idx = order(k);
    selected(end+1) = idx; %#ok<AGROW>
    running = running + weighted(idx);
    if numel(selected) >= min_channels && (running / total) >= retention_target
        break;
    end
end

selected = sort(selected);
result.selected_indices = selected;
result.retained_ratio = running / total;
end
